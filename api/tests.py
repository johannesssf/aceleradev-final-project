from django.core.exceptions import ValidationError
from django.test import TestCase

from model_bakery import baker

from .models import User


class TestUser(TestCase):

    def setUp(self):
        self.user = baker.make('api.User')
        self.user.full_clean()

    def test_user_creation(self):
        self.assertEqual(self.user, User.objects.get(id=self.user.id))

    def test_user_invalid_email(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(
                email="invalid.email",
                password="valid_password"
            )
            user.full_clean()

        with self.assertRaises(ValidationError):
            user = User.objects.create(
                email="invalid@email",
                password="valid_password"
            )
            user.full_clean()

    def test_user_invalid_password(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(
                email="valid@email",
                password="passwd"
            )
            user.full_clean()
