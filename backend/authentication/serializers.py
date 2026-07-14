from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CampainUser, UserProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CampainUser.objects.get(email=email)
        except CampainUser.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CampainUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CampainUser.objects.create_user(**validated_data, password=password)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampainUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'date_of_birth', 'bio')


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CampainUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'profile')

    def get_profile(self, obj):
        try:
            return UserProfileSerializer(obj.profile).data
        except UserProfile.DoesNotExist:
            return None


class UserWithProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        user = self.instance
        if CampainUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def update(self, instance, validated_data):
        profile_fields = ('first_name', 'last_name', 'date_of_birth', 'bio')

        for field in ('email', 'first_name', 'last_name'):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        if any(field in validated_data for field in profile_fields):
            profile, _ = UserProfile.objects.get_or_create(user=instance)

            if 'first_name' in validated_data:
                profile.first_name = validated_data['first_name']
            if 'last_name' in validated_data:
                profile.last_name = validated_data['last_name']
            if 'date_of_birth' in validated_data:
                profile.date_of_birth = validated_data['date_of_birth']
            if 'bio' in validated_data:
                profile.bio = validated_data['bio']

            profile.save()

        return instance

    def to_representation(self, instance):
        return UserWithProfileSerializer(instance).data
