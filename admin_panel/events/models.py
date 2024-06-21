from botuser.models import BotUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from notifications.models import Notification


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Event start time'
    )
    stream_link = models.URLField(blank=True)

    is_complete = models.BooleanField(
        default=False,
        help_text=(
            'Check this box if you have completed creating the event'
        )
    )
    do_broadcast = models.BooleanField(
        default=False,
        help_text=('Check this box only if you want '
                   'to start sending the event link')
    )
    users = models.ManyToManyField(BotUser, through='BotUserEvent')

    def clean(self):
        if (self.is_complete or self.do_broadcast) and not self.stream_link:
            raise ValidationError(
                'Please, add a link to the event to complete'
            )

        if (self.is_complete or self.do_broadcast) and not self.date:
            raise ValidationError(
                'Please, add date to complete'
            )

        if self.do_broadcast and self.date <= timezone.now():
            raise ValidationError(
                'Please, change date to complete'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.title[:50]}...'


class BotUserEvent(models.Model):
    class RemindType(models.IntegerChoices):
        HOUR = 0, 'Hour'
        IN_MOMENT = 1, 'In_moment'
        LINK_READY = 2, 'Link is ready'

    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    notification_type = models.PositiveSmallIntegerField(
        choices=RemindType.choices,
        blank=True
    )

    class Meta:
        verbose_name = 'User event_handlers'
        verbose_name_plural = 'User events'
        unique_together = ['user', 'event', 'notification_type']

    def __str__(self):
        return f'{self.user} in {self.event.title}'


class EventNotification(Notification):
    class EventNotificationType(models.IntegerChoices):
        HOUR_BEFORE_EVENT_NOTIFICATION = (
            0,
            'An hour before event notification'
        )
        IN_MOMENT_BEFORE_EVENT_NOTIFICATION = (
            1,
            'In moment before event notification'
        )
        NOTIFY_IMMEDIATELY = 2, 'Notify immediately'
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    notification_type = models.PositiveSmallIntegerField(
        choices=EventNotificationType.choices
    )

    class Meta:
        verbose_name = 'Event notification'
        verbose_name_plural = 'Event notifications'
        unique_together = ['event', 'notification_type']

    def clean(self):
        if not self.event.is_complete:
            raise ValidationError(
                'Please, complete Event first'
            )

        if self.event.date <= timezone.now():
            raise ValidationError(
                'Please, correct event time'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(EventNotification, self).save(*args, **kwargs)

    def __repr__(self):
        return 'Event notification'
