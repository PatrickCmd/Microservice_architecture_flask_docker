# services/users/project/tests/test_users.py


import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_admin


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users_ping(self):
        """Ensure the ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        add_admin("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "patocmd",
                        "email": "patocmd@mail.com",
                        "password": "testpassword",
                    }
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("patocmd@mail.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        add_admin("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object doesn't have a username key."""
        add_admin("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"email": "patocmd@mail.com", "password": "testpassword"}
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        add_admin("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "patocmd",
                        "email": "patocmd@mail.com",
                        "password": "testpassword",
                    }
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "patocmd",
                        "email": "patocmd@mail.com",
                        "password": "testpassword",
                    }
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user("patocmd", "patocmd@mail.com", "testpassword")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("patocmd", data["data"]["username"])
            self.assertIn("patocmd@mail.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get(f"/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User ID should be an integer", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if an id does not exist"""
        with self.client:
            response = self.client.get(f"/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user("patocmd", "patocmd@mail.com", "testpassword")
        add_user("rhenah", "rhenah@mail.com", "testpassword")
        with self.client:
            response = self.client.get(f"/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("success", data["status"])
            self.assertTrue(data["data"]["users"][0]["active"])
            self.assertFalse(data["data"]["users"][0]["admin"])
            self.assertTrue(data["data"]["users"][1]["active"])
            self.assertFalse(data["data"]["users"][1]["admin"])

    def test_index_no_users(self):
        """Ensure the index route behaves correctly when no users have been
        added to the database."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_index_with_users(self):
        """Ensure the index route behaves correctly when users have been
        added to the database."""
        add_user("michael", "michael@mherman.org", "testpassword")
        add_user("fletcher", "fletcher@notreal.com", "testpassword")
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"michael", response.data)
            self.assertIn(b"fletcher", response.data)

    def test_index_add_user(self):
        """
        Ensure a new user can be added to the database via a POST request.
        """
        with self.client:
            response = self.client.post(
                "/",
                data=dict(
                    username="patocmd",
                    email="patocmd@mail.com",
                    password="testpassword",
                ),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"patocmd", response.data)

    def test_add_user_invalid_json_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password keygraphene.
        """
        add_admin("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps(dict(username="patocmd", email="patocmd@mail.com")),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_inactive(self):
        add_user("testuser", "test@test.com", "test1234")
        # update user
        user = User.query.filter_by(email="test@test.com").first()
        user.active = False
        db.session.commit()
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "patocmd",
                        "email": "patocmd@mail.com",
                        "password": "testpassword",
                    }
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token.")

    def test_add_user_not_admin(self):
        add_user("testuser", "test@test.com", "test1234")
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test1234"}),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "patocmd",
                        "email": "patocmd@mail.com",
                        "password": "testpassword",
                    }
                ),
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "You do not have permission to do that.")


if __name__ == "__main__":
    unittest.main()
