from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


def notification_directory_path(
        instance: "NotificationContent",
        filename: str
) -> str:
    return "{}_{}/{}".format(
        repr(instance.notification), instance.notification.id, filename
    )


def get_type(file_name: str) -> str:
    valid_file_types = {
        '.gif': 'animation',
        '.m4a': 'audio',
        '.mp3': 'audio',
        '.ogg': 'audio',
        '.mp4': 'video',
        '.jpeg': 'photo',
        '.png': 'photo',
        '.jpg': 'photo',
    }
    suffix = Path(file_name).suffix.lower()

    return valid_file_types.get(suffix) or 'document'


class Notification(models.Model):
    text = models.TextField(blank=True)
    preview = models.BooleanField(
        default=True,
        help_text='Preview. Send message only to admin chat'
    )
    message_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Custom notification time if needed'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f'{self.text[:50]}...'


class NotificationContent(models.Model):
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name='media'
    )
    content_type = models.CharField(max_length=128, blank=True)
    file = models.FileField(
        upload_to=notification_directory_path, blank=True, default=None
    )
    add_to_group = models.BooleanField(
        default=False,
        help_text=('check for adding photo or video '
                   'to group in notification')
    )
    has_spoiler = models.BooleanField(
        default=False, verbose_name='Spoiler style'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notification content'
        verbose_name_plural = 'Notifications content'

    def clean(self):
        self.content_type = get_type(self.file.name)
        valid_size = 50

        if self.content_type == 'image':
            valid_size = 10

        if self.file.size > valid_size * 1024**2:
            raise ValidationError('This file is too large')

        if (self.add_to_group
                and self.content_type not in (
                    'image', 'photo', 'animation', 'video'
                )):
            raise ValidationError('You can only add '
                                  'photo or video content to group')
        if (self.has_spoiler
                and self.content_type not in (
                    'image', 'photo', 'animation', 'video'
                )):
            raise ValidationError('Spoiler animation only for '
                                  'photo or video content')

    def save(self, *args, **kwargs):
        self.content_type = get_type(self.file.name)
        self.full_clean()
        super(NotificationContent, self).save(*args, **kwargs)
