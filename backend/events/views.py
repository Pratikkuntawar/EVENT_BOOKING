

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer

# Check organizer role
def is_organizer(user):
    return user.is_authenticated and user.role == 'Organizer'


class EventUnifiedView(APIView):
    """
    Handles:
    - GET /events/ → all events (public)
    - GET /events/?category=Music → filter by category (public)
    - GET /events/?my_events=true → organizer’s events (auth required)
    - GET /events/<pk>/ → event details (public)
    - POST /events/ → create event (organizer only)
    - PUT /events/<pk>/ → update event (organizer only)
    - DELETE /events/<pk>/ → delete event (organizer only)
    """

    def get_permissions(self):
        """Allow GET for everyone, but restrict POST/PUT/DELETE."""
        if self.request.method == "GET":
            return [permissions.AllowAny()]   # no login required
        return [permissions.IsAuthenticated()]  # auth required for others

    def get(self, request, pk=None):
        if pk:  # Single event detail
            event = get_object_or_404(Event, pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # List all events
        events = Event.objects.all()
        category = request.GET.get('category', '')
        my_events = request.GET.get('my_events', '').lower()

        if category:
            events = events.filter(category__iexact=category)

        if my_events == 'true':
            if not is_organizer(request.user):
                raise PermissionDenied("Only organizers can view their events.")
            events = events.filter(organizer=request.user)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not is_organizer(request.user):
            raise PermissionDenied("Only organizers can create events.")
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not is_organizer(request.user) or event.organizer != request.user:
            raise PermissionDenied("You can only update your own events.")
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not is_organizer(request.user) or event.organizer != request.user:
            raise PermissionDenied("You can only delete your own events.")
        event.delete()
        return Response({"message": "Event deleted."}, status=status.HTTP_204_NO_CONTENT)
