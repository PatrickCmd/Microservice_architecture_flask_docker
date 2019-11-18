# service/users/project/tests/test_user_model.py

import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_passwords_are_random(self):
        user_one = add_user("testuser", "test@test.com", "testpassword")
        user_two = add_user("testuser2", "test2@test.com", "testpassword")
        self.assertNotEqual(user_one.password, user_two.password)

    def test_add_user(self):
        user = add_user("testuser", "test@test.com", "testpassword")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user("testuser", "test@test.com", "testpassword")
        duplicate_user = User(
            username="testuser", email="test2@test.com", password="testpassword"
        )
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_add_user_duplicate_email(self):
        add_user("testuser", "test@test.com", "testpassword")
        duplicate_user = User(
            username="testuser2", email="test@test.com", password="testpassword"
        )
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_to_json(self):
        user = add_user("testuser", "test@test.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_encode_auth_token(self):
        user = add_user("testuser", "test@test.com", "testpassword")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user("testuser", "test@test.com", "testpassword")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)


if __name__ == "__main__":
    unittest.main()
