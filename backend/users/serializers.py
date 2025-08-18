from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
User = CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser #telling DRF that this serializer is based on customUser Modal
        fields = ['id', 'username', 'email', 'password', 'role']#fields for serializing (coverting python onject into json)

    def create(self, validated_data):#Aand this called create method defined in customusermanager
        return CustomUser.objects.create_user(**validated_data)#** is req to convert python obj into json data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email']#this fields values get

User = CustomUser






class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user