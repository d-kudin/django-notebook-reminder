#/website/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from website.models import Record, Category
from datetime import datetime
from django.utils.timezone import make_aware 

class RecordModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test Category")
        self.record = Record.objects.create(
            user=self.user,
            title="Test Title",
            content="This is a test note content.",
            category=self.category,
            deadline=make_aware(datetime(2025, 12, 31, 12, 0)),  
            status_color='yellow',
            is_priority=True,
            reminder=make_aware(datetime(2025, 12, 25, 10, 0)) 
        )

    def test_record_creation(self):
        """Test that a Record object is created with correct values."""
        self.assertEqual(self.record.title, "Test Title")
        self.assertEqual(self.record.content, "This is a test note content.")
        self.assertEqual(self.record.user.username, "testuser")
        self.assertEqual(self.record.category.name, "Test Category")
        self.assertEqual(self.record.status_color, "yellow")
        self.assertTrue(self.record.is_priority)

    def test_record_default_values(self):
        """Test default values of the Record model."""
        self.assertFalse(self.record.is_completed)
        self.assertIsNotNone(self.record.created_at)

class CategoryModelTest(TestCase):

    def test_category_creation(self):
        """Test that a Category object is created correctly."""
        category = Category.objects.create(name="New Category")
        self.assertEqual(category.name, "New Category")
