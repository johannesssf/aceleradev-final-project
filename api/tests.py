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

    def test_record_str(self):
        rec = baker.make('api.Record')
        self.assertTrue(f'[{rec.level}]' in str(rec))

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
        """Ensure a non-existing user is not able to authenticate.
        """
        data = {'username': "non-user", 'password': "somepass1243"}
        resp = self.client.post('/api/auth/token/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class TestUsersAPI(TestCase):
    def setUp(self):
        self.users = ['john', 'beth']

        for user in self.users:
            User.objects.create_user(
                username=user,
                email=f'{user}@email.com',
                password='asdf1243'
            )

        client = APIClient()
        data = {'username': 'john', 'password': 'asdf1243'}
        resp = client.post('/api/auth/token/', data, format='json')
        self.token = resp.data['token']

    def test_users_get(self):
        """Ensure that a get in '/api/users/' works fine with a valid
        token and returns an OK status code and all existing users.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(self.users))

    def test_users_get_without_token(self):
        """Ensure that a get in '/api/users/' without a valid token will
        return an unauthorized status code.
        """
        client = APIClient()
        resp = client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_get_with_invalid_token(self):
        """Ensure that a get in '/api/users/' with an invalid token will
        return an unauthorized status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = client.get('/api/users/')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post(self):
        """Ensure that a post in '/api/users/' with valid token and
        parameters will return an created status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_users_post_without_token(self):
        """Ensure that a post in '/api/users/' without a valid token will
        return an unauthorized status code.
        """
        client = APIClient()
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post_with_invalid_token(self):
        """Ensure that a post in '/api/users/' with an invalid token will
        return an unauthorized status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        data = {
            'username': 'mary',
            'email': 'mary@mail.com',
            'password': 'asdf1234'
        }
        resp = client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post_with_invalid_parameter(self):
        """Ensure that a post in '/api/users/' with invalid parameters will
        return an bad request status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'nome': 'mary',
            'email': 'mary@mail.com',
            'senha': 'asdf1234'
        }
        resp = client.post('/api/users/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_id_get(self):
        """Ensure that a get in '/api/users/{id}' works fine with a valid
        token and returns an OK status code and the user data.
        """
        user = User.objects.latest('id')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.get(f'/api/users/{user.id}/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], user.username)
        self.assertEqual(resp.data['email'], user.email)

    def test_users_id_get_inexistent_user(self):
        """Ensure that a get in '/api/users/{id}' with a valid token
        returns an NOT FOUND status code if user's id doesn't exist.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.get('/api/users/9999/')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_id_get_without_token(self):
        """Ensure that a get in '/api/users/{id}' without a token will
        return an unauthorized status code.
        """
        user = User.objects.latest('id')
        client = APIClient()
        resp = client.post(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_get_with_invalid_token(self):
        """Ensure that a get in '/api/users/{id}' with an invalid token
        will return an unauthorized status code.
        """
        user = User.objects.latest('id')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = client.post(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_delete(self):
        """Ensure that a delete in '/api/users/{id}' works fine with a
        valid token and returns an OK status code and the user is deleted.
        """
        user = User.objects.latest('id')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=user.id)

    def test_users_id_delete_inexistent_user(self):
        """Ensure that a delete in '/api/users/{id}' with a valid token
        returns an NOT FOUND code if the user's id doesn't exist.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.delete('/api/users/9999/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_id_delete_without_token(self):
        """Ensure that a delete in '/api/users/{id}' without a token will
        return an unauthorized status code.
        """
        user = User.objects.latest('id')
        client = APIClient()
        resp = client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_id_delete_with_invalid_token(self):
        """Ensure that a delete in '/api/users/{id}' with an invalid token
        will return an unauthorized status code.
        """
        user = User.objects.latest('id')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token some-invalid-token')
        resp = client.delete(f'/api/users/{user.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRecordAPI(TestCase):
    def setUp(self):
        self.username = 'mary'
        self.email = 'mary@email.com'
        self.password = 'asdf1243'

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        client = APIClient()
        data = {'username': self.username, 'password': self.password}
        resp = client.post('/api/auth/token/', data, format='json')
        self.token = resp.data['token']

        for _ in range(3):
            baker.make(Record)

    def test_records_get_list(self):
        """Ensure that a get in '/api/records/' with a valid token will
        return a list with all available records.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.get('/api/records/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Record.objects.count(), len(resp.data))

    def test_records_get_without_token(self):
        """Ensure that a get in '/api/records/' without a token will
        return an unauthorized status code.
        """
        client = APIClient()
        resp = client.get('/api/records/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_get_with_invalid_token(self):
        """Ensure that a get in '/api/records/' with an invalid token will
        return an unauthorized status code.
        """
        client = APIClient()
        resp = client.get('/api/records/', format='json')
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'someinvalidtoken')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_post(self):
        """Ensure that a post in '/api/records/' with a valid token will
        create a new record and return a created status code.
        """
        client = APIClient()
        data = {
            'environment': 'Homologation',
            'level': 'warning',
            'message': 'some warning message',
            'origin': '192.168.0.111',
            'is_archived': False,
            'date': '2020-04-01T11:54:37',
            'user_id': User.objects.first().id
        }
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.post('/api/records/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_records_post_missing_parameters(self):
        """Ensure that a post in '/api/records/' with a valid token and
        missing required parameters will return a bad request status code.
        """
        client = APIClient()
        data = {
            'environment': 'Homologation',
            'level': 'warning',
            'message': 'some warning message',
            'origin': '192.168.0.111',
            'is_archived': False
        }
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.post('/api/records/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_records_post_non_existing_user(self):
        """Ensure that a post in '/api/records/' with a valid token and
        an invalid user id will return a bad request status code.
        """
        client = APIClient()
        data = {
            'environment': 'Homologation',
            'level': 'warning',
            'message': 'some warning message',
            'origin': '192.168.0.111',
            'is_archived': False,
            'date': '2020-04-01T11:54:37',
            'user_id': 1000
        }
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.post('/api/records/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_records_post_without_token(self):
        """Ensure that a post in '/api/records/' without a token will
        return an unauthorized status code.
        """
        client = APIClient()
        data = {
            'environment': 'Homologation',
            'level': 'warning',
            'message': 'some warning message',
            'origin': '192.168.0.111',
            'is_archived': False,
            'date': '2020-04-01T11:54:37',
            'user_id': User.objects.first().id
        }
        resp = client.post('/api/records/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_post_with_invalid_token(self):
        """Ensure that a post in '/api/records/' with an invalid token
        will return an unauthorized status code.
        """
        client = APIClient()
        data = {
            'environment': 'Homologation',
            'level': 'warning',
            'message': 'some warning message',
            'origin': '192.168.0.111',
            'is_archived': False,
            'date': '2020-04-01T11:54:37',
            'user_id': User.objects.first().id
        }
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'someinvalidtoken')
        resp = client.post('/api/records/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_get(self):
        """Ensure that a get in '/api/records/{id}/' with a valid token
        and an existent record id will return the record data.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        record = Record.objects.first()
        resp = client.get(f'/api/records/{record.id}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(record.id, resp.data['id'])
        self.assertEqual(record.level, resp.data['level'])
        self.assertEqual(record.origin, resp.data['origin'])

    def test_records_id_get_non_existent_record(self):
        """Ensure that a get in '/api/records/{id}/' with a non-existent
        record id will return a not found status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.get('/api/records/1000/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_records_id_get_without_token(self):
        """Ensure that a get in '/api/records/{id}/' without a token will
        return a unauthorized status code.
        """
        client = APIClient()
        resp = client.get('/api/records/1/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_get_invalid_token(self):
        """Ensure that a get in '/api/records/{id}/' with an invalid
        token will return a unauthorized status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'someinvalidtoken')
        resp = client.get('/api/records/1/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_put(self):
        """Ensure that a put in '/api/records/{id}/' with a valid token
        will update the record fields and return a ok status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'environment': 'New env',
            'level': 'error',
            'message': 'updated message',
            'origin': '172.169.0.50',
        }
        resp = client.put('/api/records/1/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['environment'], data['environment'])
        self.assertEqual(resp.data['level'], data['level'])
        self.assertEqual(resp.data['message'], data['message'])
        self.assertEqual(resp.data['origin'], data['origin'])

    def test_records_id_put_invalid_field_data(self):
        """Ensure that a put in '/api/records/{id}/' with a valid token
        and invalid field data will return a bad request status code.
        """
        client = APIClient()
        data = {'level': 'invalid'}

        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.put('/api/records/1/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'origin': 'a.b.c.d'}
        resp = client.put('/api/records/1/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_records_id_put_non_existent_record(self):
        """Ensure that a put in '/api/records/{id}/' with a valid token
        and an invalid record id will return a not found status code.
        """
        client = APIClient()
        data = {'level': 'info'}

        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.put('/api/records/1000/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_records_id_put_without_token(self):
        """Ensure that a put in '/api/records/{id}/' without a token will
        return a unauthorized status code.
        """
        client = APIClient()
        data = {'level': 'info'}
        resp = client.put('/api/records/1/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_put_invalid_token(self):
        """Ensure that a put in '/api/records/{id}/' with an invalid
        token will return a unauthorized status code.
        """
        client = APIClient()
        data = {'level': 'info'}
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'someinvalidtoken')
        resp = client.get('/api/records/1/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_delete(self):
        """Ensure that a delete in '/api/records/{id}/' with a valid
        token will delete the record and return a ok status code.
        """
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.delete('/api/records/1/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_records_id_delete_non_existent_record(self):
        """Ensure that a delete in '/api/records/{id}/' with a valid
        token and an invalid record id will return a not found status
        code.
        """
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = client.delete('/api/records/1000/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_records_id_delete_without_token(self):
        """Ensure that a delete in '/api/records/{id}/' without a token
        will return a unauthorized status code.
        """
        client = APIClient()
        resp = client.delete('/api/records/1/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_records_id_delete_invalid_token(self):
        """Ensure that a delete in '/api/records/{id}/' with an invalid
        token will return a unauthorized status code.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'someinvalidtoken')
        resp = client.delete('/api/records/1/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
