from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BACKEND_DIR.parent

for candidate in (SRC_DIR, BACKEND_DIR):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from backend.db.base import Base
from backend.db.session import get_db
from backend.api.routes import auth, users
from backend.api.routes import history
from backend.models.user import User
from backend.models.chat import Chat
from backend.core.security import hash_password


app = FastAPI()
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(history.router, prefix="/history")


class UserAuthSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.TestingSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=cls.engine,
        )
        Base.metadata.create_all(bind=cls.engine)

        def override_get_db():
            db = cls.TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()

    def create_test_user(
        self,
        email: str,
        password: str,
        role: str = "Employee",
        display_name: str = "Test User",
    ) -> None:
        db = self.TestingSessionLocal()
        try:
            user = User(
                email=email,
                display_name=display_name,
                password_hash=hash_password(password),
                role=role,
                issuer="test-suite",
                oidc_subject=None,
                is_active=True,
            )
            db.add(user)
            db.commit()
        finally:
            db.close()

    def test_register_login_and_me_flow(self) -> None:
        self.create_test_user(
            email="employee@greenleaf.ch",
            password="supersecret",
            display_name="Green Leaf",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "employee@greenleaf.ch",
                "password": "supersecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        login_payload = login_response.json()
        self.assertIn("access_token", login_payload)
        self.assertEqual(login_payload["token_type"], "bearer")
        self.assertEqual(login_payload["user"]["email"], "employee@greenleaf.ch")

        me_response = self.client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {login_payload['access_token']}"},
        )
        self.assertEqual(me_response.status_code, 200)
        auth_context = me_response.json()
        self.assertEqual(auth_context["email"], "employee@greenleaf.ch")
        self.assertEqual(auth_context["role"], "Employee")
        self.assertEqual(auth_context["auth_method"], "jwt")

    def test_admin_can_run_user_crud_flow(self) -> None:
        self.create_test_user(
            email="admin@greenleaf.ch",
            password="adminsecret",
            role="Admin",
            display_name="Admin User",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "admin@greenleaf.ch",
                "password": "adminsecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {admin_token}"}

        create_response = self.client.post(
            "/users",
            headers=auth_headers,
            json={
                "email": "managed.user@greenleaf.ch",
                "display_name": "Managed User",
                "password": "managedsecret",
                "role": "Employee",
                "is_active": True,
            },
        )
        self.assertEqual(create_response.status_code, 201)
        created_user = create_response.json()
        managed_user_id = created_user["id"]
        self.assertEqual(created_user["email"], "managed.user@greenleaf.ch")

        list_response = self.client.get("/users", headers=auth_headers)
        self.assertEqual(list_response.status_code, 200)
        users_payload = list_response.json()
        self.assertTrue(any(user["id"] == managed_user_id for user in users_payload))

        detail_response = self.client.get(f"/users/{managed_user_id}", headers=auth_headers)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["display_name"], "Managed User")

        update_response = self.client.put(
            f"/users/{managed_user_id}",
            headers=auth_headers,
            json={
                "display_name": "Updated Managed User",
                "role": "Admin",
                "is_active": True,
            },
        )
        self.assertEqual(update_response.status_code, 200)
        updated_user = update_response.json()
        self.assertEqual(updated_user["display_name"], "Updated Managed User")
        self.assertEqual(updated_user["role"], "Admin")

        delete_response = self.client.delete(
            f"/users/{managed_user_id}",
            headers=auth_headers,
        )
        self.assertEqual(delete_response.status_code, 204)

        missing_response = self.client.get(f"/users/{managed_user_id}", headers=auth_headers)
        self.assertEqual(missing_response.status_code, 404)

    def test_employee_cannot_access_admin_user_routes(self) -> None:
        self.create_test_user(
            email="employee2@greenleaf.ch",
            password="supersecret",
            display_name="Another Employee",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "employee2@greenleaf.ch",
                "password": "supersecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        employee_token = login_response.json()["access_token"]

        forbidden_response = self.client.get(
            "/users",
            headers={"Authorization": f"Bearer {employee_token}"},
        )
        self.assertEqual(forbidden_response.status_code, 403)

        register_response = self.client.post(
            "/auth/register",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "email": "not.allowed@greenleaf.ch",
                "password": "supersecret",
                "display_name": "Not Allowed",
            },
        )
        self.assertEqual(register_response.status_code, 403)

    def test_user_can_only_update_own_password(self) -> None:
        self.create_test_user(
            email="password.user@greenleaf.ch",
            password="oldsecret",
            display_name="Password User",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "password.user@greenleaf.ch",
                "password": "oldsecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]

        password_response = self.client.put(
            "/auth/password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "current_password": "oldsecret",
                "new_password": "newsecret",
            },
        )
        self.assertEqual(password_response.status_code, 204)

        old_login_response = self.client.post(
            "/auth/login",
            json={
                "email": "password.user@greenleaf.ch",
                "password": "oldsecret",
            },
        )
        self.assertEqual(old_login_response.status_code, 401)

        new_login_response = self.client.post(
            "/auth/login",
            json={
                "email": "password.user@greenleaf.ch",
                "password": "newsecret",
            },
        )
        self.assertEqual(new_login_response.status_code, 200)

    def test_superadmin_cannot_be_deleted_deactivated_or_demoted(self) -> None:
        self.create_test_user(
            email="superadmin@greenleaf.ch",
            password="supersecret",
            role="Admin",
            display_name="Super Admin",
        )
        self.create_test_user(
            email="other.admin@greenleaf.ch",
            password="adminsecret",
            role="Admin",
            display_name="Other Admin",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "other.admin@greenleaf.ch",
                "password": "adminsecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {admin_token}"}

        users_response = self.client.get("/users", headers=auth_headers)
        self.assertEqual(users_response.status_code, 200)
        superadmin = next(
            user
            for user in users_response.json()
            if user["email"] == "superadmin@greenleaf.ch"
        )
        superadmin_id = superadmin["id"]

        demote_response = self.client.put(
            f"/users/{superadmin_id}",
            headers=auth_headers,
            json={"role": "Employee"},
        )
        self.assertEqual(demote_response.status_code, 400)

        deactivate_response = self.client.put(
            f"/users/{superadmin_id}",
            headers=auth_headers,
            json={"is_active": False},
        )
        self.assertEqual(deactivate_response.status_code, 400)

        delete_response = self.client.delete(
            f"/users/{superadmin_id}",
            headers=auth_headers,
        )
        self.assertEqual(delete_response.status_code, 400)

    def test_history_uses_anonymous_owner_key_without_user_id(self) -> None:
        self.create_test_user(
            email="history.user@greenleaf.ch",
            password="historysecret",
            display_name="History User",
        )

        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "history.user@greenleaf.ch",
                "password": "historysecret",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}

        create_chat_response = self.client.post(
            "/history",
            headers=auth_headers,
            json={"title": "Vacation question"},
        )
        self.assertEqual(create_chat_response.status_code, 201)
        chat_payload = create_chat_response.json()
        self.assertNotIn("anonymous_user_key", chat_payload)
        chat_id = chat_payload["id"]

        create_message_response = self.client.post(
            f"/history/{chat_id}/messages",
            headers=auth_headers,
            json={
                "sender_type": "user",
                "content_masked": "Can I take vacation next week?",
            },
        )
        self.assertEqual(create_message_response.status_code, 201)

        history_response = self.client.get("/history", headers=auth_headers)
        self.assertEqual(history_response.status_code, 200)
        self.assertEqual(len(history_response.json()), 1)
        self.assertNotIn("anonymous_user_key", history_response.json()[0])

        detail_response = self.client.get(f"/history/{chat_id}", headers=auth_headers)
        self.assertEqual(detail_response.status_code, 200)
        detail_payload = detail_response.json()
        self.assertEqual(detail_payload["messages"][0]["content_masked"], "Can I take vacation next week?")

        db = self.TestingSessionLocal()
        try:
            chat = db.query(Chat).filter(Chat.id == chat_id).one()
            self.assertTrue(chat.anonymous_user_key)
            self.assertFalse(hasattr(chat, "user_id"))
        finally:
            db.close()

    def test_history_is_isolated_by_anonymous_owner_key(self) -> None:
        self.create_test_user("owner.one@greenleaf.ch", "ownersecret")
        self.create_test_user("owner.two@greenleaf.ch", "ownersecret")

        owner_one_login = self.client.post(
            "/auth/login",
            json={"email": "owner.one@greenleaf.ch", "password": "ownersecret"},
        )
        owner_two_login = self.client.post(
            "/auth/login",
            json={"email": "owner.two@greenleaf.ch", "password": "ownersecret"},
        )
        self.assertEqual(owner_one_login.status_code, 200)
        self.assertEqual(owner_two_login.status_code, 200)

        owner_one_headers = {
            "Authorization": f"Bearer {owner_one_login.json()['access_token']}"
        }
        owner_two_headers = {
            "Authorization": f"Bearer {owner_two_login.json()['access_token']}"
        }

        create_chat_response = self.client.post(
            "/history",
            headers=owner_one_headers,
            json={"title": "Private chat"},
        )
        self.assertEqual(create_chat_response.status_code, 201)
        owner_one_chat_id = create_chat_response.json()["id"]

        owner_two_list_response = self.client.get(
            "/history",
            headers=owner_two_headers,
        )
        self.assertEqual(owner_two_list_response.status_code, 200)
        self.assertEqual(owner_two_list_response.json(), [])

        owner_two_detail_response = self.client.get(
            f"/history/{owner_one_chat_id}",
            headers=owner_two_headers,
        )
        self.assertEqual(owner_two_detail_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
