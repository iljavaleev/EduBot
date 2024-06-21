from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BotAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.CharField(
        max_length=64,
        verbose_name='Add chat_id for notifications preview',
        primary_key=True
    )
    get_preview = models.BooleanField(default=False)

    def clean(self):
        if not (self.user.is_superuser or self.user.is_staff):
            raise ValidationError(
                "Bot admin must have access to the admin page. "
                "Check is_staff or is is_superuser flag"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(BotAdmin, self).save(*args, **kwargs)

    def __str__(self):
        return f"Admin chat: {self.chat_id}"


class BotUser(models.Model):
    chat_id = models.CharField(primary_key=True, max_length=64)
    get_articles = models.BooleanField(default=False)
    get_demo_week = models.BooleanField(default=False)
    username = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    first_name = models.CharField(blank=True, max_length=64, null=True)
    last_name = models.CharField(blank=True, max_length=64, null=True)
    language_code = models.CharField(blank=True, max_length=16, null=True)

    class Meta:
        verbose_name = "Bot user"
        verbose_name_plural = "Bot users"

    def __str__(self):
        return f"User: {self.chat_id}"
