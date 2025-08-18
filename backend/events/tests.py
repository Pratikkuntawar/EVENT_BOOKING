# from django.test import TestCase
# from django.utils import timezone
# from rest_framework.test import APIClient
# from rest_framework import status
# from users.models import CustomUser
# from .models import Event


# class EventAPITests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Create users
#         self.organizer = CustomUser.objects.create_user(
#             email="organizer@example.com",
#             username="organizer1",
#             password="pass123",
#             role="Organizer"
#         )
#         self.User = CustomUser.objects.create_user(
#             email="attendee@example.com",
#             username="attendee1",
#             password="pass123",
#             role="User"
#         )

#         # Create a sample event
#         self.event = Event.objects.create(
#             title="Music Concert",
#             description="Fun concert",
#             location="New York",
#             datetime=timezone.now(),
#             category="Music",
#             total_tickets=100,
#             tickets_remaining=100,
#             organizer=self.organizer
#         )

#         # URLs
#         self.list_url = "/listallevents/"
#         self.detail_url = f"/detailsofaevent/{self.event.id}/"
#         self.my_events_url = "/my-events/"
#         self.create_url = "/create-event/"
#         self.update_url = f"/update-events/{self.event.id}/"
#         self.delete_url = f"/delete-events/{self.event.id}/"

#     def test_list_all_events(self):
#         """Anyone can view list of events"""
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Music Concert")

#     def test_filter_events_by_category(self):
#         """Filtering events by category should work"""
#         response = self.client.get(self.list_url, {"category": "Music"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#         response_empty = self.client.get(self.list_url, {"category": "Sports"})
#         self.assertEqual(len(response_empty.data), 0)

#     def test_event_detail(self):
#         """Anyone can view event details"""
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["title"], "Music Concert")

#     def test_my_events_requires_authentication(self):
#         """Unauthenticated users cannot access /my-events/"""
#         response = self.client.get(self.my_events_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_my_events_as_organizer(self):
#         """Organizer should see only their events"""
#         self.client.force_authenticate(user=self.organizer)
#         response = self.client.get(self.my_events_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_my_events_as_non_organizer_fails(self):
#         """Non-organizers should get 403"""
#         self.client.force_authenticate(user=self.attendee)
#         response = self.client.get(self.my_events_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_event_as_organizer(self):
#         """Organizer can create an event"""
#         self.client.force_authenticate(user=self.organizer)
#         payload = {
#             "title": "Tech Conference",
#             "description": "Annual tech meet",
#             "location": "San Francisco",
#             "datetime": timezone.now(),
#             "category": "Technology",
#             "total_tickets": 50,
#             "tickets_remaining": 50,
#         }
#         response = self.client.post(self.create_url, payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Event.objects.count(), 2)

#     def test_create_event_as_attendee_fails(self):
#         """Attendees cannot create events"""
#         self.client.force_authenticate(user=self.attendee)
#         payload = {
#             "title": "Sports Match",
#             "description": "Exciting match",
#             "location": "LA",
#             "datetime": timezone.now(),
#             "category": "Sports",
#             "total_tickets": 50,
#             "tickets_remaining": 50,
#         }
#         response = self.client.post(self.create_url, payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_update_event_as_owner(self):
#         """Organizer can update their own event"""
#         self.client.force_authenticate(user=self.organizer)
#         payload = {"title": "Updated Concert"}
#         response = self.client.put(self.update_url, payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.event.refresh_from_db()
#         self.assertEqual(self.event.title, "Updated Concert")

#     def test_update_event_as_non_owner_fails(self):
#         """Organizers cannot update other organizers' events"""
#         other_organizer = CustomUser.objects.create_user(
#             email="org2@example.com",
#             username="organizer2",
#             password="pass123",
#             role="Organizer"
#         )
#         self.client.force_authenticate(user=other_organizer)
#         payload = {"title": "Hacked Title"}
#         response = self.client.put(self.update_url, payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_delete_event_as_owner(self):
#         """Organizer can delete their own event"""
#         self.client.force_authenticate(user=self.organizer)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Event.objects.count(), 0)

#     def test_delete_event_as_non_owner_fails(self):
#         """Non-owners cannot delete events"""
#         self.client.force_authenticate(user=self.attendee)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
