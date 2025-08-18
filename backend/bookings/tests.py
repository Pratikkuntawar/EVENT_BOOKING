from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from users.models import CustomUser
from events.models import Event
from bookings.models import Booking
from rest_framework_simplejwt.tokens import RefreshToken


class BookingAPITestCase(APITestCase):
    def setUp(self):
        # Create two users (one organizer, one normal user)
        self.organizer = CustomUser.objects.create_user(
            username="organizer",
            email="organizer@example.com",
            password="organizerpass",
            role="Organizer"
        )
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            role="User"
        )

        # Create an event owned by the organizer
        self.event = Event.objects.create(
            title="Music Concert",
            description="A great concert",
            date=timezone.now() + timezone.timedelta(days=10),
            location="City Hall",
            tickets_total=100,
            tickets_remaining=50,
            organizer=self.organizer
        )

        # URLs
        self.book_ticket_url = reverse("book-ticket")
        self.my_bookings_url = reverse("my-bookings")
        self.event_bookings_url = reverse("eventbookings", kwargs={"pk": self.event.id})
        self.user_recent_bookings_url = reverse("usersrecent-bookings")

        # Helper for auth token
        self.user_token = self.get_access_token(self.user)
        self.organizer_token = self.get_access_token(self.organizer)

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_headers(self, token):
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_book_ticket_success(self):
        payload = {"event": self.event.id, "ticket_count": 2}
        response = self.client.post(
            self.book_ticket_url, payload, format="json", **self.auth_headers(self.user_token)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.event.refresh_from_db()
        self.assertEqual(self.event.tickets_remaining, 48)  # 50 - 2

    def test_book_ticket_not_enough_tickets(self):
        payload = {"event": self.event.id, "ticket_count": 999}
        response = self.client.post(
            self.book_ticket_url, payload, format="json", **self.auth_headers(self.user_token)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_my_bookings_list(self):
        Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        response = self.client.get(self.my_bookings_url, **self.auth_headers(self.user_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_event_bookings_only_for_organizer(self):
        Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        # Organizer should see the booking
        url = reverse("eventbookings", kwargs={"pk": self.event.id})
        response = self.client.get(url, **self.auth_headers(self.organizer_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Normal user should get an empty list
        response_user = self.client.get(url, **self.auth_headers(self.user_token))
        self.assertEqual(len(response_user.data), 0)

    def test_cancel_booking_success(self):
        booking = Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        url = reverse("cancel-bookings", kwargs={"pk": booking.id})
        response = self.client.delete(url, **self.auth_headers(self.user_token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.event.refresh_from_db()
        self.assertEqual(self.event.tickets_remaining, 53)  # 50 + 3 back

    def test_cancel_booking_not_owner(self):
        booking = Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        url = reverse("cancel-bookings", kwargs={"pk": booking.id})
        response = self.client.delete(url, **self.auth_headers(self.organizer_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_export_bookings_json(self):
        Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        url = reverse("export-bookings", kwargs={"format": "json"})
        response = self.client.get(url, **self.auth_headers(self.user_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_export_bookings_csv(self):
        Booking.objects.create(user=self.user, event=self.event, ticket_count=3)
        url = reverse("export-bookings", kwargs={"format": "csv"})
        response = self.client.get(url, **self.auth_headers(self.user_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_user_recent_bookings(self):
        for _ in range(5):
            Booking.objects.create(user=self.user, event=self.event, ticket_count=1)
        response = self.client.get(self.user_recent_bookings_url, **self.auth_headers(self.user_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 10)

