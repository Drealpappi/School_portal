from rest_framework import serializers
from django.db import transaction
from accounts.models import User
from accounts.serializers import UserSerializer
from academics.models import ClassRoom, AcademicSession
from .models import Student, Parent, Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    Student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    admission_number = serializers.CharField(source='student.user.admission_number', read_only=True)
    class_room = serializers.CharField(source='class_room.__str__', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'student_name',
            'admission_number',
            'class_room',
            'class_room_name',
            'session', 'session_name',
            'status'
        ]
class StudentReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_enrollment = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'admission_number',
            'gender',
            'address'
            'admission_date',
            'current_enrolment'
        ]

    def get_current_enrollment(self, obj):
        enrollments = getattr(obj, 'active_enrollments', None)
        if enrollments is not None:
            enrollment = enrollments[0] if enrollments else None
        else:
            enrollment = obj.enrollments.filter(session__is_current=True).select_related('class_room__level', 'session').first()
        return EnrollmentSerializer(enrollment).data if enrollment else None

class StudentCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=60, write_only=True)
    last_name = serializers.CharField(max_length=60, write_only=True)
    password = serializers.CharField(write_only=True, required=False)
    class_room_id = serializers.CharField(write_only=True, required=False)
    session_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Student
        field = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'admission_number',
            'date_of_birth',
            'gender',
            'address',
            'class_room_id',
            'session_id'
        ]

    def validate_email(self, value):
        if User.objects.filter(email__isexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')
        class_room_id = validated_data.pop('class_room_id')
        session_id = validated_data.pop('session_id')

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=User.Role.STUDENT,
            password=password
        )

        student = Student.objects.create(user=user, **validated_data)

        if class_room_id and session_id:
            Enrollment.objects.create(
                student=student,
                class_room_id=class_room_id,
                session_id=session_id,
                status=Enrollment.Status.ACTIVE
            )
        return student