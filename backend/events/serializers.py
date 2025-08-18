
from rest_framework import serializers
from .models import Event, CustomUser
import cloudinary.uploader

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    image_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'tickets_remaining']

    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            validated_data['image_url'] = upload_result['secure_url']
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_file', None)
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            validated_data['image_url'] = upload_result['secure_url']
        return super().update(instance, validated_data)
