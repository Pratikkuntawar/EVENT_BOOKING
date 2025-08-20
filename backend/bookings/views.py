

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
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
        Handle multiple GET operations based on query parameters
        Example:
          /api/booking/book-ticket/?action=my_bookings
          /api/booking/book-ticket/?action=event_bookings&event_id=2  (only organizer can perform this action)
          /api/booking/book-ticket/?action=recent_bookings
          /api/booking/book-ticket/?action=export_json
        """
        action = request.query_params.get("action")
        user = request.user

        if action == "my_bookings":
            bookings = Booking.objects.filter(user=user)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        elif action == "event_bookings":
            # ✅ Only organizers allowed
            if not hasattr(user, "role") or user.role != "organizer":
                return Response(
                    {"error": "You are not allowed to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            event_id = request.query_params.get("event_id")
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
