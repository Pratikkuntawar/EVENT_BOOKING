from rest_framework import serializers
from .models import Event
from .models import CustomUser
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'
#         read_only_fields = ['organizer', 'tickets_remaining']






# class OrganizerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email']  # Add other fields if needed

# class EventSerializer(serializers.ModelSerializer):
#     organizer = OrganizerSerializer(read_only=True)

#     class Meta:
#         model = Event
#         fields = '__all__'
#         read_only_fields = ['organizer', 'tickets_remaining']
#below code from line 28 to 58 is to store base 64 string in url
# import base64
# from rest_framework import serializers
# from .models import Event, CustomUser

# class OrganizerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email']

# class EventSerializer(serializers.ModelSerializer):
#     organizer = OrganizerSerializer(read_only=True)
#     image_file = serializers.ImageField(write_only=True, required=False)  # file input

#     class Meta:
#         model = Event
#         fields = '__all__'
#         read_only_fields = ['organizer', 'tickets_remaining']

#     def create(self, validated_data):
#         image_file = validated_data.pop('image_file', None)
#         if image_file:
#             encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#             validated_data['image_base64'] = encoded_string
#         return Event.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         image_file = validated_data.pop('image_file', None)
#         if image_file:
#             encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#             validated_data['image_base64'] = encoded_string
#         return super().update(instance, validated_data)
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
