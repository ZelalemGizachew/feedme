from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import User
from .serializers import *

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'update', 'partial_update'):
            return [IsAuthenticated()]  # Allow only authenticated users for list, retrieve, update, and partial update
        elif self.action == 'create':
            return [AllowAny()]  # Allow anyone to create a new user without authentication
        return [IsAdminUser()]  # Allow only admin for other actions

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.queryset.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user == instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response("You do not have permission to view this profile.", status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            serializer = UserCreateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("You do not have permission to update this profile.", status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        is_exist = User.objects.filter(email=email).exists()
        if is_exist:
            return Response("Your account already exists!", status=status.HTTP_409_CONFLICT)

        serializer = UserCreateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # Print detailed validation errors to the console
            print(f"Validation Errors: {e.detail}")
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BusinessClosingViewSet(ModelViewSet):
    queryset = BusinessClosing.objects.all()
    serializer_class = BusinessClosingSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]  # Only authenticated users can create
        elif self.action in ['list', 'retrieve']:
            return [IsAdminUser()]  # Only staff users can list all details
        else:
            return [IsAuthenticated()]  # For other actions, only authenticated users are allowed

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            # Staff users can list all details
            queryset = self.queryset.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Non-staff users can only list their own details
            queryset = self.queryset.filter(user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user == instance.user:
            # Staff users can retrieve any details, non-staff users can only retrieve their own details
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response("You do not have permission to view this detail.", status=status.HTTP_403_FORBIDDEN)

# {
#     "businessName": "Test",
#     "businessType": "Test",
#     "longitude": "1234.123",
#     "latitude": "1234.123",
#     "contactPersonName": "Zola",
#     "phoneNumber": "+251912345678",
#     "email": "zola@gmail.com",
#     "password": "ILoveDjango"
# }