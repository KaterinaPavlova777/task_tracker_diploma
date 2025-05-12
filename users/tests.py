from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import Task
from users.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='regularpass123',
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Do something',
            performer=self.regular_user,
            deadline='2025-06-15'
        )

    def authenticate(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_UserRegistration(self):
        data = {
            'username': 'newuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_UserListView(self):
        self.authenticate(self.admin_user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_UserDetailView(self):
        self.authenticate(self.regular_user)
        response = self.client.get(f'/users/{self.regular_user.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UserUpdateView(self):
        self.authenticate(self.admin_user)
        data = {'username': 'updatedname'}
        response = self.client.patch(f'/users/update/{self.regular_user.pk}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'updatedname')

    def test_UserDeleteView(self):
        self.authenticate(self.admin_user)
        user_to_delete = User.objects.create_user(
            username='delete_me',
            password='delpass123'
        )
        response = self.client.delete(f'/users/delete/{user_to_delete.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user_to_delete.pk).exists())

    def test_UserWithTaskListView(self):
        user1 = User.objects.create_user(username='user1', password='p1')
        user2 = User.objects.create_user(username='user2', password='p2')
        Task.objects.create(title='T1', performer=user1, deadline='2025-06-15')
        Task.objects.create(title='T2', performer=user1, deadline='2025-06-15')
        Task.objects.create(title='T3', performer=user2, deadline='2025-06-15')

        self.authenticate(self.admin_user)
        response = self.client.get('/users/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], user1.username)
        self.assertEqual(response.data[1]['username'], user2.username)

    def test_CandidateForTaskListView_returns_candidates_for_important_task(self):
        from users.services import get_users_for_imp_task
        candidates = get_users_for_imp_task()

        self.authenticate(self.admin_user)
        response = self.client.get('/users/candidate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(candidates))
