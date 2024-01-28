from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import BusinessClosing


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['businessName', 'businessType', 'longitude', 'latitude', 'contactPersonName', 'phoneNumber', 'email', 'password']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        # fields = ('__all__')
        fields = ['id', 'businessName', 'businessType', 'longitude', 'latitude', 'contactPersonName', 'phoneNumber', 'email', 'isVerified', 'createdOn', 'updatedOn']
        ref_name = 'djoser_user'

class BusinessClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessClosing
        fields = ['day', 'time']

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token