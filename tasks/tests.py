from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import Task
from users.models import User


class TasksTestCase(APITestCase):

    def setUp(self):
        self.user_regular = User.objects.create_user(
            username="regular", password="testpass123", access_level=1
        )
        self.user_admin = User.objects.create_superuser(
            username="admin", password="testpass123", access_level=60
        )
        self.task1 = Task.objects.create(
            title="Task 1",
            description="Description 1",
            status="created",
            deadline="2025-06-15",
            performer=self.user_regular,
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="Description 2",
            deadline="2025-06-15",
            status="in_progress",
        )
        self.task3 = Task.objects.create(
            title="Important Task",
            description="Needs attention",
            status="created",
            deadline="2025-06-15",
            parent=self.task2,
        )

    def authenticate(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_TaskListView(self):
        self.authenticate(self.user_regular)
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_TaskDetailView(self):
        self.authenticate(self.user_regular)
        response = self.client.get(f"/tasks/{self.task1.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task1.title)

    def test_TaskCreateView(self):
        self.authenticate(self.user_admin)
        data = {
            "title": "New Task",
            "description": "Do something",
            "deadline": "2025-06-15",
            "status": "created",
        }
        response = self.client.post("/tasks/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_TaskUpdateView(self):
        self.authenticate(self.user_admin)
        data = {"title": "Updated Title"}
        response = self.client.patch(f"/tasks/update/{self.task1.pk}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Updated Title")

    def test_TaskDeleteView(self):
        self.authenticate(self.user_admin)
        response = self.client.delete(f"/tasks/delete/{self.task3.pk}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task3.pk).exists())

    def test_ImportantTaskListView(self):
        self.authenticate(self.user_regular)
        response = self.client.get("/tasks/important/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Important Task")
