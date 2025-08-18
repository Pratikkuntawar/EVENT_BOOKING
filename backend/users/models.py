from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='User'):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)# this coverts the the domain part of email into lowercase
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)#this is where password is hashed before data storing into the database (Django hashed password automatically)
        user.save(using=self._db)#this us where data is saved into database
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Organizer', 'Organizer'),#left right Organiser will saved in database and right side Organiser for admin panel
        ('User', 'User'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'#Tells Django to use email instead of username for authentication.bydefault django perform login via username(bydefault:username is req for login)
    REQUIRED_FIELDS = ['username']#django will ask for username while creating superuser

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        db_table = 'custom_user_table'  


