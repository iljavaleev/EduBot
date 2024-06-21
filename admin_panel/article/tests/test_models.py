from unittest import mock

from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.test import TestCase
from django.utils import timezone

from ..models import ArticleNotification


class ArticleNotificationModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.article = ArticleNotification.objects.create(
            title='Test',
            text='......................mock_text................'
                 '.....................mock_text...........',
            preview=False
        )

    def test_default_values(self):
        article = ArticleNotification.objects.create(
            title='Test',
            text='Check this box only if you',
            preview=False
        )
        self.assertEqual(article.notify_immediately, False)

    def test_str_repr(self):
        article = ArticleNotificationModelTest.article
        self.assertEqual(str(article), f'{article.text[:50]}...')

    def test_article_notification_past_time(self):
        article = ArticleNotificationModelTest.article
        article.message_time = timezone.now() - timezone.timedelta(hours=1)
        self.assertRaises(
            ValidationError,
            article.save,
        )

    def test_notify_immediately_and_message_time_collision(self):
        article = ArticleNotificationModelTest.article
        article.message_time = timezone.now() + timezone.timedelta(days=1)
        article.notify_immediately = True
        self.assertRaises(
            ValidationError,
            article.save,
        )

    @mock.patch('article.signals.create_article_notification_task')
    def test_do_broadcast(self, create_article_notification_task):
        article = ArticleNotification(
            title='Test',
            text='text',
            preview=False,
            notify_immediately=True,
            is_complete=True
        )
        post_save.send(
            sender=ArticleNotification,
            instance=article,
            created=False
        )
        create_article_notification_task.assert_called_once()

    @mock.patch('article.signals.delete_article_notification_with_task')
    def test_delete_task_signal(self, delete_news_notification_with_task):
        article = ArticleNotificationModelTest.article
        post_delete.send(
            sender=ArticleNotification,
            instance=article,
        )
        delete_news_notification_with_task.assert_called_once()
