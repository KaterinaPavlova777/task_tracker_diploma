from django.db.models import Count
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserWithTaskSerializer,
    TaskCandidateSerializer,
)
from users.services import get_users_for_imp_task


class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return UserSerializer
        return UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserWithTaskListView(ListAPIView):
    serializer_class = UserWithTaskSerializer

    def get_queryset(self):
        return User.objects.annotate(tasks_count=Count("tasks")).order_by(
            "-tasks_count"
        )


class CandidateForTaskListView(ListAPIView):
    serializer_class = TaskCandidateSerializer

    def list(self, request, *args, **kwargs):
        queryset = get_users_for_imp_task()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
