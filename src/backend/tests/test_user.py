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
from backend.models.user import User
from backend.core.security import hash_password


app = FastAPI()
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")


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


if __name__ == "__main__":
    unittest.main()
