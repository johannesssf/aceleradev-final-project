from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase

from model_bakery import baker

from rest_framework import status
from rest_framework.test import APIClient

from .models import Record


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


class TestAuthTokenAPI(TestCase):

    def setUp(self):
        self.username = 'joe'
        self.email = 'joe@email.com'
        self.password = 'asdf1243'
        self.client = APIClient()

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_api_auth_token(self):
        """Ensure a system user is able to authenticate and get his token.
        """
        data = {'username': self.username, 'password': self.password}
        resp = self.client.post('/api/auth/token/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_api_auth_token_invalid_credentials(self):
        """Ensure a non-existing user is able to authenticate.
        """
        data = {'username': "non-user", 'password': "somepass1243"}
        resp = self.client.post('/api/auth/token/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class TestUsersAPI(TestCase):
    def setUp(self):
        self.users = ['john', 'beth']
        self.client = APIClient()

        for user in self.users:
            User.objects.create_user(
                username=user,
                email=f'{user}@email.com',
                password='asdf1243'
            )

        data = {'username': 'john', 'password': 'asdf1243'}
        resp = self.client.post('/api/auth/token/', data, format='json')
        self.token = resp.data['token']

    def test_users_get(self):
        """Ensure that a get in '/api/users/' works fine with a valid
        token and returns an OK status code and all existing users.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(self.users))

    def test_users_get_without_token(self):
        """Ensure that a get in '/api/users/' without a valid token will
        return an unauthorized status code.
        """
        resp = self.client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_get_with_invalid_token(self):
        """Ensure that a get in '/api/users/' with an invalid token will
        return an unauthorized status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = self.client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post(self):
        """Ensure that a post in '/api/users/' with valid token and
        parameters will return an created status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = self.client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_users_post_without_token(self):
        """Ensure that a post in '/api/users/' without a valid token will
        return an unauthorized status code.
        """
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = self.client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post_with_invalid_token(self):
        """Ensure that a post in '/api/users/' with an invalid token will
        return an unauthorized status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = self.client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post_with_invalid_parameter(self):
        """Ensure that a post in '/api/users/' with invalid parameters will
        return an bad request status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'nome': 'mary',
            'email': 'mary@mail.com',
            'senha': 'asdf1234'
        }
        resp = self.client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_id_get(self):
        """Ensure that a get in '/api/users/{id}' works fine with a valid
        token and returns an OK status code and the user data.
        """
        user = User.objects.latest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get(f'/api/users/{user.id}/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], user.username)
        self.assertEqual(resp.data['email'], user.email)

    def test_users_id_get_inexistent_user(self):
        """Ensure that a get in '/api/users/{id}' with a valid token
        returns an NOT FOUND status code if user's id doesn't exist.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.get('/api/users/9999/')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_id_get_without_token(self):
        """Ensure that a get in '/api/users/{id}' without a token will
        return an unauthorized status code.
        """
        user = User.objects.latest('id')
        resp = self.client.post(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_get_with_invalid_token(self):
        """Ensure that a get in '/api/users/{id}' with an invalid token
        will return an unauthorized status code.
        """
        user = User.objects.latest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = self.client.post(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_delete(self):
        """Ensure that a delete in '/api/users/{id}' works fine with a
        valid token and returns an OK status code and the user is deleted.
        """
        user = User.objects.latest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=user.id)

    def test_users_id_delete_inexistent_user(self):
        """Ensure that a delete in '/api/users/{id}' with a valid token
        returns an NOT FOUND code if the user's id doesn't exist.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.delete('/api/users/9999/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_id_delete_without_token(self):
        """Ensure that a delete in '/api/users/{id}' without a token will
        return an unauthorized status code.
        """
        user = User.objects.latest('id')
        resp = self.client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_delete_with_invalid_token(self):
        """Ensure that a delete in '/api/users/{id}' with an invalid token
        will return an unauthorized status code.
        """
        user = User.objects.latest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = self.client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
