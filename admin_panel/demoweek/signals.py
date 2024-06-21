from celeryapp.utils import create_preview_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DemoDay


@receiver(post_save, sender=DemoDay)
def save_demo_day(sender, instance: DemoDay, created, **kwargs):
    if instance.preview:
        create_preview_task(instance=instance)
