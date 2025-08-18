from rest_framework import serializers
from .models import Booking
from events.models import Event
from events.serializers import EventSerializer

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['id', 'user', 'event', 'ticket_count', 'booked_at']
#         read_only_fields = ['user', 'booked_at']

#     def validate(self, data):
#         event = data['event']
#         requested = data['ticket_count']

#         if requested > event.tickets_remaining:
#             raise serializers.ValidationError("Not enough tickets available.")
#         return data


class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source='event', write_only=True#we used source=event here becuase user will pass only event id then it will map to whole event in response body
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'event_id', 'ticket_count', 'booked_at']  # Add event_id here
        read_only_fields = ['user', 'booked_at']#if i comment this line then postman will asked for user filed in request obj


