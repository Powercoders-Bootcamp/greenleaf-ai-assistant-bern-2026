from __future__ import annotations

import sys
import unittest
from pathlib import Path

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
from backend.main import app


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

    def test_register_login_and_me_flow(self) -> None:
        register_response = self.client.post(
            "/auth/register",
            json={
                "email": "employee@greenleaf.ch",
                "password": "supersecret",
                "display_name": "Green Leaf",
            },
        )
        self.assertEqual(register_response.status_code, 201)
        registered_user = register_response.json()
        self.assertEqual(registered_user["email"], "employee@greenleaf.ch")
        self.assertEqual(registered_user["role"], "Employee")
        self.assertTrue(registered_user["is_active"])

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


if __name__ == "__main__":
    unittest.main()
