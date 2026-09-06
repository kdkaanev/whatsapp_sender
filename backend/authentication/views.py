from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from app.tasks import send_activation_email
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
    UserWithProfileSerializer,
    UserWithProfileUpdateSerializer,
)
from .models import CampainUser, UserProfile


class RegisterView(generics.CreateAPIView):
    queryset = CampainUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = serializer.instance
        send_activation_email.delay(user.id)  # Send activation email asynchronously    
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                'message': 'Login successful',
                'tokens': response.data
            }, status=status.HTTP_200_OK)
        return response


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserWithProfileUpdateSerializer
        return UserWithProfileSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        try:
            instance.profile.delete()
        except UserProfile.DoesNotExist:
            pass

class ActivateView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CampainUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CampainUser.DoesNotExist):
            return Response(
                {'error': 'Invalid activation link'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {'error': 'Invalid or expired activation link'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response(
            {'message': 'Account activated successfully'},
            status=status.HTTP_200_OK
        )