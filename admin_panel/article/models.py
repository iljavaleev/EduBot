from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from notifications.models import Notification


class ArticleNotification(Notification):
    title = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    notify_immediately = models.BooleanField(default=False)
    is_complete = models.BooleanField(
        default=False,
        help_text='Check if you have finished creating article',
    )

    class Meta:
        verbose_name = 'Article notification'
        verbose_name_plural = 'Articles notification'

    def clean(self):
        if (self.message_time is not None
                and self.message_time < timezone.now()):
            raise ValidationError(
                'Please, correct message time'
            )

        if self.message_time is not None and self.notify_immediately:
            raise ValidationError(
                'Please, choose between message '
                'in scheduled time and immediate notification'
            )

        if (self.notify_immediately or self.message_time) and \
                not self.is_complete:
            raise ValidationError('Please complete article to notify users')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ArticleNotification, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.text[:50]}...'

    def __repr__(self):
        return 'Article notification'
