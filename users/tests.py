from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customers as UserC
from rest_framework.authtoken.models import Token


class AccountsTestCase(APITestCase):
    """
    Тестирование процесса создания пользователя
    """

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = UserC.objects.create_user(username='testuser', email='test@example.com',
                                                   password='testpassword', phone=48216, date_of_birth='1999-02-20')

        # URL for creating an account.
        self.create_url = reverse('account-create')

    def test_create_user(self):
        """
        Создание пользователя и проверка создания токена
        """
        data = {
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password': 'somepassword',
                'phone': 586183,
                'date_of_birth': '1999-02-20'
                }

        response = self.client.post(self.create_url, data, format='json')
        # user = UserC.objects.latest('id')
        # token = Token.objects.get(user=user)
        self.assertEqual(UserC.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        # self.assertEqual(response.data['token'], token.key)
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Проверка создания пользователя с коротким паролем
        """
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': 'foo',
                'phone': 588983,
                'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Создание пользователя без пароля
        :return:
        """
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': '',
                'phone': 5151515,
                'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        """
        Создание пользователя с длинным паолем
        :return:
        """
        data = {
            'username': 'foo' * 30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar',
            'phone': 589815,
            'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        """
        Создание пользователя без ника
        :return:
        """
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar',
            'phone': 588925,
             'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        """
        Создание пользователя с уже существующим ником
        :return:
        """
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'testuser',
            'phone': 8416158,
            'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        """
        Создание пользователя с уже существующим email
        :return:
        """
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser',
            'phone': 841618,
            'date_of_birth': '1999-02-20'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        """
        Создание пользователя с неправильным email
        :return:
        """
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz',
            'phone': 8419163,
            'date_of_birth': '1999-02-20'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        """
        Создание пользователя без email
        :return:
        """
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz',
                'phone': 8481358,
                'date_of_birth': '1999-02-20'

        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_phone(self):
        """
        Создание пользователя без телефона
        :return:
        """
        data = {
                'username': 'foobarcust',
                'email': 'foobarcust@example.com',
                'password': 'foobarbaz',
                'phone': (),
                'date_of_birth': '1999-02-20'

        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserC.objects.count(), 1)
        self.assertEqual(len(response.data['phone']), 1)


if __name__ == '__main__':
    APITestCase.run()