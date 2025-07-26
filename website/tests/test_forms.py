#/website/tests/test_forms.py


from django.test import TestCase
from website.forms import RecordForm
from website.models import Category
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime

class RecordFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_record_form_valid_data(self):
        """Form should be valid when all required fields are correctly filled."""
        form = RecordForm(data={
            'title': 'Test title',
            'content': 'Test note content.',
            'deadline': make_aware(datetime(2025, 12, 31, 12, 0)),
            'reminder': make_aware(datetime(2025, 12, 25, 10, 0)),
            'is_priority': True,
            'status_color': 'yellow',
            'category': self.category.id,
        })
        self.assertTrue(form.is_valid())

    def test_record_form_missing_required_fields(self):
        """Form should be invalid if required fields are missing."""
        form = RecordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)

    def test_record_form_invalid_color_choice(self):
        """Form should be invalid if status_color has invalid value."""
        form = RecordForm(data={
            'title': 'Title',
            'content': 'Content',
            'status_color': 'invalid_color',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('status_color', form.errors)

    def test_record_form_optional_fields(self):
        """Form should be valid even if optional fields are not provided."""
        form = RecordForm(data={
            'title': 'Note without deadline and reminder',
            'content': 'Note content',
            'status_color': 'yellow',
            'category': self.category.id,
        })
        self.assertTrue(form.is_valid())

