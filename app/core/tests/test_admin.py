"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.db.utils import IntegrityError
from django.db import transaction

from psycopg2.errors import UniqueViolation


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client"""
        try:
            self.client = Client()
            with transaction.atomic():
                self.admin_user = get_user_model().objects.create_superuser(
                    email='admin@example.com',
                    password='testpass123'
                )
                self.client.force_login(self.admin_user)

                self.user = get_user_model().objects.create_user(
                    email='user@example.com',
                    password='testpass123',
                    username='pablo',
                    name='Test User'
                )

        except (UniqueViolation, IntegrityError):
            print("User already exists")
            self.user = get_user_model().objects.get(email='user@example.com')

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.admin_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
