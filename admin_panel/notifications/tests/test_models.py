from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import Notification, NotificationContent


class NotificationModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.notification = Notification.objects.create(
            text='__________...........Notification'
                 '...........______________.......................',
        )

    def test_default_values(self):
        notification = NotificationModelTest.notification
        self.assertEqual(notification.preview, True)

    def test_do_broadcast_help_text(self):
        notification = NotificationModelTest.notification
        self.assertEqual(
            notification._meta.get_field('preview').help_text,
            'Preview. Send message only to admin chat'
        )
        self.assertEqual(
            notification._meta.get_field('message_time').help_text,
            'Custom notification time if needed'
        )

    def test_str_repr(self):
        notification = NotificationModelTest.notification
        self.assertEqual(str(notification), f'{notification.text[:50]}...')


class NotificationContentModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.n_content = NotificationContent.objects.create(
            notification=Notification.objects.create(text='Some text'),
            file=SimpleUploadedFile(
                'document.doc',
                b'these are the file content'
            )
        )

    def test_default_values(self):
        n_content = NotificationContentModelTest.n_content
        self.assertEqual(n_content.add_to_group, False)
        self.assertEqual(n_content.has_spoiler, False)

    def test_add_to_group_help_text(self):
        n_content = NotificationContentModelTest.n_content
        self.assertEqual(
            n_content._meta.get_field('add_to_group').help_text,
            'check for adding photo or video to group in notification'
        )

    def test_has_spoiler_verbose(self):
        n_content = NotificationContentModelTest.n_content
        self.assertEqual(
            n_content._meta.get_field('has_spoiler').verbose_name,
            'Spoiler style'
        )

    def generate_sample_file(self):
        sample_file_names = (
            'doc.txt',
            'doc.doc',
            'audio.m4a',
            'audio.mp3',
            'audio.ogg',
        )
        for name in sample_file_names:
            file = NotificationContent.objects.create(
                notification=Notification.objects.create(text='Some text'),
                file=SimpleUploadedFile(
                    name=name,
                    content=b'these are the file content'
                )
            )
            yield file

    def test_add_to_group(self):
        for file in self.generate_sample_file():
            with self.subTest():
                file.add_to_group = True
                self.assertRaises(
                    ValidationError,
                    file.save
                )

    def test_has_spoiler(self):
        for file in self.generate_sample_file():
            with self.subTest():
                file.has_spoiler = True
                self.assertRaises(
                    ValidationError,
                    file.save
                )
