"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.db.utils import IntegrityError
from django.db import transaction

from core.models import User

from psycopg2.errors import UniqueViolation

from unittest.mock import patch


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
        except (UniqueViolation, IntegrityError):
            print("User already exists")
        self.user = User(email='user@examp.com', password='testpass123', name='Test User')

    @patch('django.test.Client.get')
    def test_users_list(self, patched_get):
        """Test that users are listed on page."""
        patched_get.return_value = [
            {
                'name': 'Test User',
                'email': 'user@example.com'
            }
        ]

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
