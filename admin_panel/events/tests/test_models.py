from unittest import mock

from botuser.models import BotUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from ..models import BotUserEvent, Event, EventNotification


class EventModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = Event.objects.create(
            title='...........................Test '
                  'event_handlers.............................'
        )

    def test_str_repr(self):
        self.assertEqual(str(EventModelTest.event),
                         f'{EventModelTest.event.title[:50]}...')

    def test_verbose_date(self):
        event = EventModelTest.event
        self.assertEqual(
            event._meta.get_field('date').verbose_name,
            'Event start time'
        )

    def test_do_broadcast_help_text(self):
        event = EventModelTest.event
        self.assertEqual(
            event._meta.get_field('do_broadcast').help_text,
            'Check this box only if you want to '
            'start sending the event link'
        )

    def test_default_values(self):
        event = EventModelTest.event
        self.assertEqual(event.do_broadcast, False)

    def test_do_broadcast_without_date(self):
        event = EventModelTest.event
        event.stream_link = 'mock@link.ru'
        event.do_broadcast = True
        self.assertRaises(
            ValidationError,
            EventModelTest.event.save,
        )

    def test_do_broadcast_without_link(self):
        event = EventModelTest.event
        event.date = timezone.now() + timezone.timedelta(hours=1)
        event.do_broadcast = True
        self.assertRaises(
            ValidationError,
            EventModelTest.event.save,
        )

    @mock.patch('events.signals.send_event_task_construct')
    def test_do_broadcast_task(self, send_event_task_construct):
        event = EventModelTest.event
        event.do_broadcast = True

        post_save.send(
            sender=Event,
            instance=event,
            created=False
        )
        send_event_task_construct.assert_called_once()


class BotUserEventModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bot_user_event = BotUserEvent.objects.create(
            user=BotUser.objects.create(chat_id='12345'),
            event=Event.objects.create(title='Event_title'),
            notification_type=0,
        )

    def test_str_repr(self):
        bte = BotUserEventModelTest.bot_user_event
        self.assertEqual(str(bte), f'{bte.user} in {bte.event.title}')

    def test_unique_together_constraint(self):
        bte = BotUserEventModelTest.bot_user_event
        self.assertRaises(
            IntegrityError,
            BotUserEvent.objects.create,
            user=bte.user,
            event=bte.event,
            notification_type=bte.notification_type
        )


class EventNotificationModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event_notification = EventNotification.objects.create(
            event=Event.objects.create(
                title='Event_title',
                date=timezone.now() + timezone.timedelta(hours=1)
            ),
            notification_type=0,
            preview=False,
        )

    def test_event_notification_for_event_without_date(self):
        event_not = EventNotificationModelTest.event_notification
        event_not.event.date = None
        self.assertRaises(
            ValidationError,
            event_not.save,
        )

    def test_unique_together_constraint(self):
        event_not = EventNotificationModelTest.event_notification
        self.assertRaises(
            ValidationError,
            EventNotification.objects.create,
            event=event_not.event,
            notification_type=event_not.notification_type
        )

    @mock.patch('events.signals.create_before_event_notification_task')
    def test_hour_before(self, create_before_event_notification_task):
        event_not = EventNotification(
            event=Event.objects.create(
                title='Event_title',
                date=timezone.now() + timezone.timedelta(hours=1)
            ),
            notification_type=EventNotification.EventNotificationType
            .HOUR_BEFORE_EVENT_NOTIFICATION.value,
            preview=False,
        )

        post_save.send(
            sender=EventNotification,
            instance=event_not,
            created=False
        )
        create_before_event_notification_task.assert_called_once()

    @mock.patch('events.signals.create_before_event_notification_task')
    def test_moment_before(self, create_before_event_notification_task):
        event_not = EventNotification(
            event=Event.objects.create(
                title='Event_title',
                date=timezone.now() + timezone.timedelta(hours=1)
            ),
            notification_type=EventNotification.EventNotificationType
            .IN_MOMENT_BEFORE_EVENT_NOTIFICATION.value,
            preview=False,
        )

        post_save.send(
            sender=EventNotification,
            instance=event_not,
            created=False
        )
        create_before_event_notification_task.assert_called_once()

    @mock.patch('events.signals.send_event_task_construct')
    def test_immediate(self, send_event_task_construct):
        event_not = EventNotification(
            event=Event.objects.create(
                title='Event_title',
                date=timezone.now() + timezone.timedelta(hours=1)
            ),
            notification_type=EventNotification.EventNotificationType
            .NOTIFY_IMMEDIATELY.value,
            preview=False,
        )
        post_save.send(
            sender=EventNotification,
            instance=event_not,
            created=False
        )
        send_event_task_construct.assert_called_once()

    @mock.patch('events.signals.delete_event_notification_with_task')
    def test_delete_task_signal(self, delete_event_notification_with_task):
        event_not = EventNotificationModelTest.event_notification

        post_delete.send(
            sender=EventNotification,
            instance=event_not,
        )
        delete_event_notification_with_task.assert_called_once()
