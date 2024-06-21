from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import CuratorChat


class CuratorChatModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chat_id = '12345'
        cls.curator_chat = CuratorChat.objects.create(chat_id='12345')

    def test_default_values(self):
        self.assertEqual(CuratorChatModelTest.curator_chat.is_active, False)

    def test_unique_active_curator_chat(self):
        CuratorChatModelTest.curator_chat.is_active = True
        CuratorChatModelTest.curator_chat.save()

        self.assertRaises(
            ValidationError,
            CuratorChat.objects.create,
            chat_id='345678',
            is_active=True
        )

    def test_str_repr(self):
        curator_chat = CuratorChatModelTest.curator_chat
        self.assertEqual(
            str(curator_chat),
            f'Curator chat: {curator_chat.chat_id}'
        )
