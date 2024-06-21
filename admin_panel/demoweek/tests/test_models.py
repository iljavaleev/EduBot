from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import DemoDay


class DemoDayModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.demo_day = DemoDay.objects.create(preview=False)

    def test_default_values(self):
        self.assertEqual(DemoDayModelTest.demo_day.weekday, 7)

    def test_multiple_example_day(self):
        another_demo_day = DemoDay.objects.create(preview=False)
        self.assertEqual(
            DemoDayModelTest.demo_day.weekday,
            another_demo_day.weekday
        )

    def test_unique_week_day(self):
        DemoDayModelTest.demo_day.weekday = 1
        DemoDayModelTest.demo_day.save()
        self.assertRaises(
            ValidationError,
            DemoDay.objects.create,
            weekday=1,
            preview=False,
        )
