from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

from tasks.serializers import TaskSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = "__all__"


class UserWithTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["full_name", "tasks", "tasks_count"]

    def get_tasks_count(self, obj: User):
        return obj.tasks.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["full_name", "password"]
        validators = [validate_password]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("full_name", instance.username)
        password = validated_data.get("password")
        if password:
            instance.password = password
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "full_name", "password", "password_confirm")

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise ValidationError("The passwords don't match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = User.objects.create_user(
            username=validated_data["username"],
            full_name=validated_data["full_name"],
            email="",
            password=validated_data["password"],
        )
        return user


class LimitUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name"]


class TaskCandidateSerializer(serializers.Serializer):
    task = TaskSerializer()
    performer = LimitUserSerializer(source="candidate")
