from hashlib import sha256

from django.core.exceptions import ValidationError
from django.test import TestCase

from model_bakery import baker

from rest_framework.test import APIClient

from .models import User, Record


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


class TestRecord(TestCase):

    def setUp(self):
        self.record = baker.make('api.Record')

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


class TestUserAPI(TestCase):
    def setUp(self):
        self.total_users = 5
        for _ in range(self.total_users):
            baker.make(User).save()

    def test_users_get_list(self):
        client = APIClient()
        resp = client.get('/api/users/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), self.total_users)

    def test_users_post_status_201(self):
        client = APIClient()
        user = {'email': 'newuser@email.com', 'password': 'newuserpass'}
        resp = client.post('/api/users/', user)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['email'], user['email'])
        self.assertEqual(sha256(user['password'].encode()).hexdigest(),
                                resp.data['password'])

    def test_users_post_status_400(self):
        client = APIClient()
        # Invalid email
        user = {'email': 'invalid-email.com', 'password': 'newuserpass'}
        resp = client.post('/api/users/', user)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['email'][0].code, 'invalid')

        # Invalid password
        user = {'email': 'newuser@email.com', 'password': '1234'}
        resp = client.post('/api/users/', user)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['password'][0].code, 'min_length')

    def test_users_delete_status_404(self):
        client = APIClient()
        resp = client.delete('/api/users/55/')

        self.assertEqual(resp.status_code, 404)

    def test_users_delete_status_200(self):
        client = APIClient()
        user = baker.make(User)
        user.save()
        resp = client.delete(f'/api/users/{user.id}/')

        self.assertEqual(resp.status_code, 200)
