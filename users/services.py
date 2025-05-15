from django.db.models import Count

from tasks.models import Task
from users.models import User


def get_users_for_imp_task():
    free_employee = (
        User.objects.annotate(tasks_count=Count("tasks"))
        .order_by("tasks_count")
        .first()
    )

    if not free_employee:
        return []

    important_tasks = Task.objects.filter(
        status="created", parent__status="in_progress"
    )

    result = []

    for task in important_tasks:
        candidate = free_employee
        if task.parent and task.parent.performer:
            performer = task.parent.performer
            tasks_count = performer.tasks.count()
            if tasks_count <= free_employee.tasks_count + 2:
                candidate = performer

        result.append(
            {
                "task": task,
                "candidate": candidate,
            }
        )

    return result
