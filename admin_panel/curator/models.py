from django.core.exceptions import ValidationError
from django.db import models


class CuratorChat(models.Model):
    chat_id = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)

    def clean(self):
        if self.is_active and (
                CuratorChat.objects.filter(is_active=True).exists()
                and CuratorChat.objects.get(is_active=True).id != self.id
        ):
            raise ValidationError(
                'You, can create only one active curator chat instance'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CuratorChat, self).save(*args, **kwargs)

    def __str__(self):
        return f'Curator chat: {self.chat_id}'


class CuratorAnswer(models.Model):
    message_id = models.CharField(max_length=64, primary_key=True)
    chat_id = models.CharField(max_length=64)
    text = models.TextField()
