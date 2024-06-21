from django.core.exceptions import ValidationError
from django.db import models
from notifications.models import Notification


class DemoDay(Notification):
    class WeekDay(models.IntegerChoices):
        SUNDAY = 0, 'Sunday'
        MONDAY = 1, 'Monday'
        TUESDAY = 2, 'Tuesday'
        WEDNESDAY = 3, 'Wednesday'
        THURSDAY = 4, 'Thursday'
        FRIDAY = 5, 'Friday'
        SATURDAY = 6, 'Saturday'
        EXAMPLE = 7, 'Example'
    weekday = models.PositiveSmallIntegerField(
        choices=WeekDay.choices,
        default=WeekDay.EXAMPLE
    )

    class Meta:
        verbose_name = 'Demo day'
        verbose_name_plural = 'Demo days'

    def clean(self):
        if self.weekday != self.WeekDay.EXAMPLE and (
                DemoDay.objects.filter(weekday=self.weekday).exists()
                and DemoDay.objects.get(weekday=self.weekday).id != self.id
        ):
            raise ValidationError(
                'You, can create only one weekday instance'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(DemoDay, self).save(*args, **kwargs)
