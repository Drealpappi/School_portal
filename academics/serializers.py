from rest_framework import serializers
from .models import AcademicSession, Term, ClassLevel, ClassRoom, Subject, SubjectAllocation

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['id', 'name', 'start_date', 'end_date', 'is_current']

class TermSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)

    class Meta:
        model = Term
        fields = ['id', 'session', 'session_name', 'name', 'start_date', 'end_date', 'is_current']

class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = ['id', 'name', 'level_order']

class ClassRoomSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)
    form_teacher_name = serializers.CharField(source='form_teacher.user.full_name', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'level', 'level_name', 'arm', 'full_name', 'capacity', 'form_techer', 'form_teacher_name']

    def get_full_name(self, obj):
        return str(obj)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_code', 'is_core']

class SubjectAllocationSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    Subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_room_name = serializers.CharField(source='class_room.__str__', read_only=True)

    class Meta:
        model = SubjectAllocation
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name', 'class_room', 'class_room_name', 'session']