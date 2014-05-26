"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import get_stat, set_stat

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(get_stat('NONEXISTENT_STATISTIC'), None)
        set_stat('APPLE', -1.738564)
        self.assertEqual(get_stat('APPLE'), -1.738564, 0.000001)