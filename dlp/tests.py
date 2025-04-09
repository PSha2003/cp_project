from django.test import TestCase
from .models import Pattern

class PatternTest(TestCase):
    def test_create_pattern(self):
        pattern = Pattern.objects.create(name="CCN", regex=r"\\b\\d{16}\\b")
        self.assertEqual(pattern.name, "CCN")
