from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    UserRegistration,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    UserWithTaskListView,
    CandidateForTaskListView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistration.as_view(), name="register"),
    path("", UserListView.as_view(), name="users_list"),
    path("<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>", UserDeleteView.as_view(), name="user_delete"),
    path("tasks/", UserWithTaskListView.as_view(), name="user_tasks"),
    path("candidate/", CandidateForTaskListView.as_view(), name="user_candidate"),
]
