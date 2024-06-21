from django.db import models


class Task(models.Model):

    notification_id = models.PositiveIntegerField()
    uuid = models.TextField()
