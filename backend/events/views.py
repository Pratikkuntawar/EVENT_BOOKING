from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer

# Utility function to check organizer role
def is_organizer(user):
    return user.is_authenticated and user.role == 'Organizer'

# List all events (Public)#with this route we can view all organizers events
class EventListView(APIView):
    def get(self, request):
        # search = request.GET.get('search', '')
        category = request.GET.get('category', '')

        events = Event.objects.all()
        # if search:
        #     events = events.filter(title__icontains=search)
        if category:
            events = events.filter(category__iexact=category)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Event Details (Public)//with this we can view particular event details
class EventDetailView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Organizer's Events#with this organizer can see only his details
class MyEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not is_organizer(request.user):
            raise PermissionDenied("Only organizers can view their events.")
        events = Event.objects.filter(organizer=request.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create Event#organizer can create his own events
class CreateEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not is_organizer(request.user):
            raise PermissionDenied("Only organizers can create events.")

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Event#update existing events by organizer
class UpdateEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not is_organizer(request.user) or event.organizer != request.user:
            raise PermissionDenied("You can only update your own events.")

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Event #delete evnts hosted ny organizer
class DeleteEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not is_organizer(request.user) or event.organizer != request.user:
            raise PermissionDenied("You can only delete your own events OR you have not enough previledge to delete events")

        event.delete()
        return Response({"message": "Event deleted."}, status=status.HTTP_204_NO_CONTENT)

