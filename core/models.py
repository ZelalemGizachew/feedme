from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    businessName = models.CharField(max_length = 255)
    businessType = models.CharField(max_length = 255)
    longitude = models.CharField(max_length = 255)
    latitude = models.CharField(max_length = 255)
    contactPersonName = models.CharField(max_length = 255)
    phoneNumber = models.CharField(max_length = 255)
    email = models.EmailField(unique=True)
    isVerified = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # REQUIRED_FIELDS = ['businessName', 'businessType', 'longitude', 'latitude', 'contactPersonName', 'phoneNumber', 'password']
    objects = UserManager()

class BusinessClosing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_closings')
    day = models.CharField(max_length=20)
    time = models.TimeField()

    def __str__(self):
        return f"{self.user.email} - {self.day} - {self.time}"