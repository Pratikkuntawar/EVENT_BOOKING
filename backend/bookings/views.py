# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.db import transaction
# from .models import Booking
# from events.models import Event
# from .serializers import BookingSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse, HttpResponse
# import csv

# # View to handle booking tickets
# class BookTicketView(APIView):
#     permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can book

#     def post(self, request):
#         serializer = BookingSerializer(data=request.data)  # Deserialize the input data
#         if serializer.is_valid():
#             event = serializer.validated_data['event']  # Get event object from validated data
#             ticket_count = serializer.validated_data['ticket_count']  # Get number of tickets to book

#             # Check if enough tickets are available
#             if ticket_count > event.tickets_remaining:
#                 return Response({'error': 'Not enough tickets available.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Decrement available tickets
#             event.tickets_remaining -= ticket_count
#             event.save()  # Save updated ticket count

#             # Save the booking with the current user
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response

#         # If invalid data is provided
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # View to fetch current user's bookings
# class MyBookingsView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # Return all bookings that belong to the logged-in user
#     def get_queryset(self):#get_queryset() exists by default in the class-based view
#         return Booking.objects.filter(user=self.request.user)# intetnally happens like this SELECT * FROM bookings_table
# #WHERE user_id = <id_of_logged_in_user>;

# # View to fetch bookings for a specific event (only visible to event organizer)
# class EventBookingsView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         event_id = self.kwargs['pk']  # kwargs is a way to pass url parameter to class based view #Get event ID from URL
#         # Return bookings for that event made to the organizer
#         return Booking.objects.filter(event__id=event_id, event__organizer=self.request.user)

# # View to cancel a booking
# class CancelBookingView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     @transaction.atomic  # Ensures that ticket update and delete happen together #ENTIRE OPERATION ACT AS A SINGLE UNIT..EVEN THOUGH IF WE REMOVE THIS THERE WILL BE NO CHANGE
#     def delete(self, request, pk):
#         booking = generics.get_object_or_404(Booking, pk=pk)  # Get the booking to be canceled

#         # Check if the booking belongs to the current user
#         if booking.user != request.user:
#             return Response({'error': 'You can only cancel your own bookings.'}, status=status.HTTP_403_FORBIDDEN)

#         # Re-increment the event's ticket count
#         event = booking.event
#         event.tickets_remaining += booking.ticket_count
#         event.save()  # Save updated ticket count

#         booking.delete()  # Delete the booking
#         return Response({'message': 'Booking cancelled.'}, status=status.HTTP_204_NO_CONTENT)

# class ExportBookingsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user = request.user
#         bookings = Booking.objects.filter(user=user)  # or event__organizer=user if needed

#         if format == 'json':
#             serializer = BookingSerializer(bookings, many=True)
#             print("User:", user)
#             print("Bookings count:", bookings.count())
#             print("Booking IDs:", list(bookings.values_list("id", flat=True)))
#             return JsonResponse(serializer.data, safe=False)

#         return JsonResponse({'error': 'Invalid format specified. Use "csv" or "json".'}, status=400)


# class UserRecentBookingsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')[:10]
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.http import JsonResponse
from .models import Booking
from events.models import Event
from .serializers import BookingSerializer


class BookTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # ---------------- GET ----------------
    def get(self, request):
        """
        Handle multiple GET operations based on request.data['action']
        - my_bookings
        - event_bookings
        - recent_bookings
        - export_json
        """
        action = request.data.get("action")
        user = request.user

        if action == "my_bookings":
            bookings = Booking.objects.filter(user=user)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        elif action == "event_bookings":
            event_id = request.data.get("event_id")
            if not event_id:
                return Response({"error": "event_id required"}, status=400)
            bookings = Booking.objects.filter(event__id=event_id, event__organizer=user)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        elif action == "recent_bookings":
            bookings = Booking.objects.filter(user=user).order_by("-booked_at")[:10]
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        elif action == "export_json":
            bookings = Booking.objects.filter(user=user)
            serializer = BookingSerializer(bookings, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response({"error": "Invalid action"}, status=400)

    # ---------------- POST ----------------
    def post(self, request):
        """Book new tickets"""
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data['event']
            ticket_count = serializer.validated_data['ticket_count']

            if ticket_count > event.tickets_remaining:
                return Response({'error': 'Not enough tickets available.'}, status=400)

            event.tickets_remaining -= ticket_count
            event.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    # ---------------- PUT ----------------
    def put(self, request):
        """Update a booking"""
        booking_id = request.data.get("booking_id")
        if not booking_id:
            return Response({"error": "booking_id required"}, status=400)

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # ---------------- DELETE ----------------
    @transaction.atomic
    def delete(self, request):
        """Cancel a booking"""
        booking_id = request.data.get("booking_id")
        if not booking_id:
            return Response({"error": "booking_id required"}, status=400)

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        event = booking.event
        event.tickets_remaining += booking.ticket_count
        event.save()

        booking.delete()
        return Response({"message": "Booking cancelled."}, status=204)
