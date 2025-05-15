from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ImportantTaskListView,
)

app_name = TasksConfig.name

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("update/<int:pk>", TaskUpdateView.as_view(), name="task_update"),
    path("delete/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),
    path("important/", ImportantTaskListView.as_view(), name="task_important_list"),
]
