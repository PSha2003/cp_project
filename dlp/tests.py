from django.test import TestCase
from .models import Pattern

class PatternTest(TestCase):
    def setUp(self):
        self.pattern = Pattern.objects.create(
            name="CCN",
            regex=r"\\b\\d{16}\\b",
        )
    def test_create_pattern(self):
        #pattern = Pattern.objects.create(name="CCN", regex=r"\\b\\d{16}\\b")
        self.assertEqual(self.pattern.name, "CCN")

    def test_pattern_matching(self):
        """Test the regex pattern matching works as expected"""
        result = self.pattern.matches("1234567812123434")
        self.assertTrue(result)
        
        result = self.pattern.matches("abcd-ef-ghij")
        self.assertFalse(result)
