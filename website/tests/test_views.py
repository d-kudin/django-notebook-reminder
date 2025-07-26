#/website/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import Record, Category
from django.utils.timezone import now, timedelta

class HomeViewTest(TestCase):

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

class AddRecordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.client.login(username='testuser', password='testpass')

    def test_add_record_view(self):
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_record.html')

    def test_add_record_form_submission(self):
        response = self.client.post(reverse('add_record'), {
            'title': 'New note',
            'content': 'New note content',
            'deadline': '',
            'reminder': '',
            'is_priority': False,
            'status_color': 'yellow',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Record.objects.count(), 1)

class UpdateRecordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.record = Record.objects.create(
            user=self.user,
            title='Old note',
            content='Old note content',
            category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_update_record_view(self):
        response = self.client.get(reverse('update_record', args=[self.record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_record.html')

    def test_update_record_form_submission(self):
        response = self.client.post(reverse('update_record', args=[self.record.id]), {
            'title': 'Updated Note',
            'content': 'Updated content',
            'deadline': '',
            'reminder': '',
            'is_priority': False,
            'status_color': 'green',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)
        updated_record = Record.objects.get(id=self.record.id)
        self.assertEqual(updated_record.title, 'Updated Note')

class DeleteRecordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.record = Record.objects.create(
            user=self.user,
            title='Note to Delete',
            content='Content to be deleted',
            category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_delete_record_view(self):
        response = self.client.get(reverse('delete_record', args=[self.record.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Record.objects.count(), 0)

class FilterRecordsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category1 = Category.objects.create(name="Work")
        self.category2 = Category.objects.create(name="Home")
        Record.objects.create(user=self.user, title="Work - Report", content="Content 1", category=self.category1)
        Record.objects.create(user=self.user, title="Home - Groceries", content="Content 2", category=self.category2)
        self.client.login(username='testuser', password='testpass')

    def test_filter_by_category(self):
        response = self.client.get(reverse('home'), {'category': self.category1.id})
        self.assertContains(response, "Work - Report")
        self.assertNotContains(response, "Home - Groceries")

    def test_filter_by_date(self):
        today = Record.objects.first().created_at.date().isoformat()
        response = self.client.get(reverse('home'), {'date': today})
        self.assertContains(response, "Work - Report")
        self.assertContains(response, "Home - Groceries")

class CompleteRecordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.record = Record.objects.create(
            user=self.user,
            title='Note to Complete',
            content='Note content',
            category=self.category,
            status_color='yellow',
            is_completed=False
        )
        self.client.login(username='testuser', password='testpass')

    def test_complete_record_view(self):
        response = self.client.get(reverse('complete_record', args=[self.record.id]))
        self.assertEqual(response.status_code, 302)  
        self.record.refresh_from_db()
        self.assertTrue(self.record.is_completed)
        self.assertEqual(self.record.status_color, 'green')

class ReminderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.record = Record.objects.create(
            user=self.user,
            title='Note with Reminder',
            content='Reminder content',
            category=self.category,
            reminder=now() - timedelta(minutes=5),  
            is_completed=False
        )
        self.client.login(username='testuser', password='testpass')

    def test_reminder_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Reminders')
        self.assertContains(response, 'Note with Reminder')

class RecordSortingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test category")
        self.record1 = Record.objects.create(
            user=self.user,
            title='Older Note',
            content='Content 1',
            category=self.category
        )
        self.record2 = Record.objects.create(
            user=self.user,
            title='Newer Note',
            content='Content 2',
            category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_record_ordering(self):
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        first_pos = content.find('Newer Note')
        second_pos = content.find('Older Note')
        self.assertLess(first_pos, second_pos)  
