from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import BotAdmin, BotUser

User = get_user_model()


class BotUserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bot_user = BotUser.objects.create(chat_id='12345')

    def test_default_values(self):
        bot_user = BotUserModelTest.bot_user
        self.assertEqual(bot_user.get_articles, False)
        self.assertEqual(bot_user.get_demo_week, False)

    def test_str_repr(self):
        bot_user = BotUserModelTest.bot_user
        self.assertEqual(str(bot_user), f'User: {bot_user.chat_id}')


class BotAdminModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.admin = User.objects.create_superuser(
            'admin',
            'email',
            'testpass123'
        )
        cls.bot_admin = BotAdmin.objects.create(
            user=BotAdminModelTest.admin,
            chat_id='12345'
        )

    def test_create_bot_admin_from_django_admin(self):
        self.assertRaises(
            ValidationError,
            BotAdmin.objects.create,
            user=BotAdminModelTest.user
        )

    def test_verbose_name(self):
        bot_admin = BotAdminModelTest.bot_admin
        self.assertEqual(
            bot_admin._meta.get_field('chat_id').verbose_name,
            'Add chat_id for notifications preview'
        )

    def test_default_values(self):
        bot_admin = BotAdminModelTest.bot_admin
        self.assertEqual(bot_admin.get_preview, False)

    def test_str_repr(self):
        bot_admin = BotAdminModelTest.bot_admin
        self.assertEqual(str(bot_admin), f'Admin chat: {bot_admin.chat_id}')
