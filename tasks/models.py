from django.db import models

from users.models import User

NULLABLE = {
    "null": True,
    "blank": True,
}


class Task(models.Model):
    STATUS_CHOICES = (
        ("created", "created"),
        ("in_process", "in_process"),
        ("finalized", "finalized"),
    )

    title = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(verbose_name="content", **NULLABLE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="dependencies",
        verbose_name="parent",
        **NULLABLE
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="tasks",
        verbose_name="performer",
        **NULLABLE
    )
    deadline = models.DateField(verbose_name="deadline")
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="created", verbose_name="status"
    )

    def __str__(self):
        return self.title[:15]
