from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import EventCategory, Event
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class EventCategoryTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="AdminPass123"
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="UserPass123"
        )

    def test_list_categories(self):
        EventCategory.objects.create(name="Conference", description="Tech events")
        url = reverse("events:category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_category_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("events:category-list")
        data = {"name": "Workshop", "description": "Hands-on learning"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("events:category-list")
        data = {"name": "Seminar", "description": "Educational session"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="AdminPass123"
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="UserPass123"
        )
        self.category = EventCategory.objects.create(name="Conference", description="Tech events")

    def test_list_events(self):
        Event.objects.create(
            title="Future Event",
            description="Sample",
            date=timezone.now() + timedelta(days=5),
            location="Lagos",
            category=self.category,
            created_by=self.user,
            capacity=100
        )
        url = reverse("events:event-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)  # paginated

    def test_create_event_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("events:event-list")
        data = {
            "title": "New Event",
            "description": "Created by user",
            "date": (timezone.now() + timedelta(days=3)).isoformat(),
            "location": "Abuja",
            "category": self.category.id,
            "capacity": 50
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_unauthenticated_forbidden(self):
        url = reverse("events:event-list")
        data = {
            "title": "Unauthorized Event",
            "description": "Should fail",
            "date": (timezone.now() + timedelta(days=2)).isoformat(),
            "location": "Port Harcourt",
            "category": self.category.id,
            "capacity": 20
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_event_only_creator_or_admin(self):
        event = Event.objects.create(
            title="My Event",
            description="Owned by user",
            date=timezone.now() + timedelta(days=10),
            location="Lagos",
            category=self.category,
            created_by=self.user,
            capacity=80
        )
        url = reverse("events:event-detail", args=[event.id])

        # Try with another user (not creator, not admin)
        other_user = User.objects.create_user(
            username="other", email="other@example.com", password="OtherPass123"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.put(url, {"title": "Hacked Event"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Try with admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, {"title": "Admin Updated Event"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_events_by_category(self):
        # Create two events in different categories
        workshop = EventCategory.objects.create(name="Workshop", description="Hands-on")
        Event.objects.create(
            title="Conf Event",
            description="Conference event",
            date=timezone.now() + timedelta(days=5),
            location="Lagos",
            category=self.category,
            created_by=self.user,
            capacity=50
        )
        Event.objects.create(
            title="Workshop Event",
            description="Workshop event",
            date=timezone.now() + timedelta(days=7),
            location="Abuja",
            category=workshop,
            created_by=self.user,
            capacity=30
        )

        url = reverse("events:event-list")
        response = self.client.get(url, {"category": workshop.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(ev["category"] == workshop.id for ev in response.data["results"]))

    def test_filter_events_by_date_range(self):
        # Create two events: one in 3 days, another in 15 days
        Event.objects.create(
            title="Soon Event",
            description="Happens soon",
            date=timezone.now() + timedelta(days=3),
            location="Lagos",
            category=self.category,
            created_by=self.user,
            capacity=20
        )
        Event.objects.create(
            title="Later Event",
            description="Happens later",
            date=timezone.now() + timedelta(days=15),
            location="Abuja",
            category=self.category,
            created_by=self.user,
            capacity=20
        )

        url = reverse("events:event-list")
        response = self.client.get(url, {
            "start_date": (timezone.now() + timedelta(days=1)).date(),
            "end_date": (timezone.now() + timedelta(days=7)).date()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only "Soon Event" should be in results
        titles = [ev["title"] for ev in response.data["results"]]
        self.assertIn("Soon Event", titles)
        self.assertNotIn("Later Event", titles)

    def test_pagination_on_events_list(self):
        # Create 12 events (page size = 10, so should be 2 pages)
        for i in range(12):
            Event.objects.create(
                title=f"Event {i}",
                description="Paginated test",
                date=timezone.now() + timedelta(days=i+1),
                location="Lagos",
                category=self.category,
                created_by=self.user,
                capacity=100
            )

        url = reverse("events:event-list")
        response = self.client.get(url)  # first page
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

        # Fetch second page
        next_url = response.data["next"]
        response2 = self.client.get(next_url)
        self.assertEqual(len(response2.data["results"]), 2)



# Create your tests here.
