from rest_framework import serializers
from .models import Event
from .models import CustomUser
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'
#         read_only_fields = ['organizer', 'tickets_remaining']






class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # Add other fields if needed

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'tickets_remaining']
