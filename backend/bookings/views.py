from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Booking
from events.models import Event
from .serializers import BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
import csv

# View to handle booking tickets
class BookTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can book

    @transaction.atomic  # Ensures atomicity: if one part fails, whole operation rolls back
    def post(self, request):
        serializer = BookingSerializer(data=request.data)  # Deserialize the input data
        if serializer.is_valid():
            event = serializer.validated_data['event']  # Get event object from validated data
            ticket_count = serializer.validated_data['ticket_count']  # Get number of tickets to book

            # Check if enough tickets are available
            if ticket_count > event.tickets_remaining:
                return Response({'error': 'Not enough tickets available.'}, status=status.HTTP_400_BAD_REQUEST)

            # Decrement available tickets
            event.tickets_remaining -= ticket_count
            event.save()  # Save updated ticket count

            # Save the booking with the current user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response

        # If invalid data is provided
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to fetch current user's bookings
class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Return all bookings that belong to the logged-in user
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# View to fetch bookings for a specific event (only visible to event organizer)
class EventBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['pk']  # Get event ID from URL
        # Return bookings for that event made to the organizer
        return Booking.objects.filter(event__id=event_id, event__organizer=self.request.user)

# View to cancel a booking
class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic  # Ensures that ticket update and delete happen together
    def delete(self, request, pk):
        booking = generics.get_object_or_404(Booking, pk=pk)  # Get the booking to be canceled

        # Check if the booking belongs to the current user
        if booking.user != request.user:
            return Response({'error': 'You can only cancel your own bookings.'}, status=status.HTTP_403_FORBIDDEN)

        # Re-increment the event's ticket count
        event = booking.event
        event.tickets_remaining += booking.ticket_count
        event.save()  # Save updated ticket count

        booking.delete()  # Delete the booking
        return Response({'message': 'Booking cancelled.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_bookings(request, format=None):
    user = request.user
    bookings = Booking.objects.filter(event__organizer=user)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Booking ID', 'Event Title', 'User', 'Tickets Booked', 'Booked At'])

        for booking in bookings:
            writer.writerow([
                booking.id,
                booking.event.title,
                booking.user.username,
                booking.ticket_count,
                booking.booked_at
            ])
        return response

    elif format == 'json':
        serializer = BookingSerializer(bookings, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({'error': 'Invalid format specified. Use "csv" or "json".'}, status=400)


@api_view(['GET'])#to fetch recent booking
@permission_classes([IsAuthenticated])
def user_recent_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')[:10]
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
