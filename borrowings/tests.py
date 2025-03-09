import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from books.models import Book
from borrowings.models import Borrowing


class BorrowingViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="testpass123"
        )
        self.staff_user = get_user_model().objects.create_user(
            email="staff@test.com",
            password="testpass123",
            is_staff=True
        )
        self.another_user = get_user_model().objects.create_user(
            email="another@test.com",
            password="testpass123"
        )

        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Test Author",
            inventory=5,
            daily_fee=10.00
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Test Author",
            inventory=0,
            daily_fee=15.00
        )

        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        self.borrowing = Borrowing.objects.create(
            book=self.book1,
            user=self.user,
            expected_return_date=tomorrow
        )

        self.book1.inventory -= 1
        self.book1.save()

        self.returned_borrowing = Borrowing.objects.create(
            book=self.book1,
            user=self.user,
            expected_return_date=tomorrow,
            actual_return_date=timezone.now().date()
        )

        self.client = APIClient()

    def test_create_borrowing_success(self):
        """Test creating a borrowing with valid data"""
        self.client.force_authenticate(user=self.user)

        expected_return_date = timezone.now().date() + datetime.timedelta(
            days=7
        )
        url = reverse("borrowings:borrowings-list")
        data = {
            "book": self.book1.id,
            "expected_return_date": expected_return_date
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 3)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.inventory, 3)

    def test_create_borrowing_no_inventory(self):
        """Test creating a borrowing when book has no inventory"""
        self.client.force_authenticate(user=self.user)

        expected_return_date = timezone.now().date() + datetime.timedelta(
            days=7
        )
        url = reverse("borrowings:borrowings-list")
        data = {
            "book": self.book2.id,
            "expected_return_date": expected_return_date
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book", response.data)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_borrowing_return_success(self):
        """Test successful return of a borrowed book"""
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "borrowings:borrowings-borrowing-return",
            kwargs={"pk": self.borrowing.id}
        )
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.inventory, 5)

    def test_borrowing_return_already_returned(self):
        """Test return of an already returned book"""
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "borrowings:borrowings-borrowing-return",
            kwargs={"pk": self.returned_borrowing.id}
        )
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_filter_by_is_active_true(self):
        """Test filtering borrowings by is_active=true"""
        self.client.force_authenticate(user=self.user)

        url = reverse("borrowings:borrowings-list") + "?is_active=true"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing.id)

    def test_filter_by_is_active_false(self):
        """Test filtering borrowings by is_active=false"""
        self.client.force_authenticate(user=self.user)

        url = reverse("borrowings:borrowings-list") + "?is_active=false"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.returned_borrowing.id)

    def test_filter_by_user_id_as_staff(self):
        """Test staff user can filter borrowings by user_id"""
        self.client.force_authenticate(user=self.staff_user)

        url = reverse("borrowings:borrowings-list") + f"?user_id={self.user.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_user_id_as_non_staff(self):
        """Test non-staff user can only see their own borrowings regardless of filter"""
        self.client.force_authenticate(user=self.another_user)

        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        another_borrowing = Borrowing.objects.create(
            book=self.book1,
            user=self.another_user,
            expected_return_date=tomorrow
        )

        url = reverse("borrowings:borrowings-list") + f"?user_id={self.user.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], another_borrowing.id)
