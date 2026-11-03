from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsSchoolAdmin, IsTeacherOrAdmin
from .models import Student, Enrollment
from .serializers import (
    StudentReadSerializer,
    StudentCreationSerializer,
    EnrollmentSerializer,
)

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        active_enrollment_prefetch = Prefetch(
            'enrollments',
            queryset=Enrollment.objects.filter(session_is_current=True).select_related('class_room__level', 'session'),
            to_attr='active_enrollments'
        )
        queryset = Student.objects.select_related('user').prefetch_related(active_enrollment_prefetch)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsTeacherOrAdmin()]
        return [IsSchoolAdmin()]
    
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related(
        'student__user',
        'class_room__level',
        'sessio'
    ).all()

    serializer_class = EnrollmentSerializer
    permission_classes = [IsSchoolAdmin]

    @action(detail=False, methods=['post'], url_path='promote-students')
    def promote_students(self, request):
        student_ids = request.data.get('student_ids', [])
        target_class_room_id = request.data.get('target_class_room_id')
        target_seesion_id = request.data.get('target_session_id')

        if not (student_ids and target_class_room_id and target_seesion_id):
            return Response({"detail": "Student_ids, target_class_room_id, and target_session_id are required."}, status=status.HTTPS_400_BAD_REQUEST)

        enrollments_to_create = [
            Enrollment(
                student_id=s_id,
                class_room_id=target_class_room_id,
                session_id=target_seesion_id,
                status=Enrollment.Status.ACTIVE
            )
            for s_id in student_ids
        ]

        Enrollment.objects.bulk_create(enrollments_to_create, ingnore_conflicts=True)
        return Response({"detail": f"Successfully enrolled {len(enrollments_to_create)} students."}, status=status.HTTPS_201_CREATED)