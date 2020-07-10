from django.core.exceptions import ValidationError
from django.test import TestCase

from model_bakery import baker

from .models import User, Record


class TestUser(TestCase):

    def setUp(self):
        self.user = baker.make('api.User')
        self.user.full_clean()
        print(self.user)

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


class TestRecord(TestCase):

    def setUp(self):
        self.record = baker.make('api.Record')
        print(self.record)

    def test_record_creation(self):
        self.assertEqual(self.record, Record.objects.get(id=self.record.id))

    def test_record_invalid_level(self):
        with self.assertRaises(ValidationError):
            rec = baker.make('api.Record')
            rec.level = 'invalid_one'
            rec.full_clean()

    def test_record_invalid_oring(self):
        with self.assertRaises(ValidationError):
            rec = baker.make('api.Record')
            rec.origin = 'a.b.c.d'
            rec.full_clean()
