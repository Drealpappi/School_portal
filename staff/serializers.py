from django.db import transaction
from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import StaffProfile

class StaffProfileReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StaffProfile
        fields = ['id', 'user', 'staff_id', 'qualification', 'date_joined_school', 'address', 'created_at']

class StaffCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=40, write_only=True)
    last_name = serializers.CharField(max_length=40, write_only=True)
    phone_number = serializers.CharField(max_length=15, required=False, blank=True, write_only=True)
    role = serializers.ChoiceField(choices=[User.Role.TEACHER, User.Role.ACCOUNTANT, User.Role.ADMIN], default=User.Role.TEACHER, write_only=True)

    password = serializers.CharField(min_length=8, required=False, write_only=True)

    class Meta:
        model = StaffProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'staff_id', 'password', 'qualification', 'date_joined_school', 'address', 'created_at']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exist.")
            return value

    @transaction.atomic
    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        phone_number = validated_data.pop('phone_number', '')
        role = validated_data.pop('role', User.Role.TEACHER)
        password = validated_data.pop('password', 'StaffPass123!')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            role=role,
            password=password
            
        )

        staff = StaffProfile.objects.create(user=user, **validated_data)
        return staff