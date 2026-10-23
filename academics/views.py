from django.shortcuts import render
from rest_framework import viewsets
from core.permissions import IsSchoolAdmin
from rest_framework.permissions import IsAuthenticated
from .models import AcademicSession, Term, ClassLevel, ClassRoom, Subject, SubjectAllocation
from .serializers import AcademicSessionSerializer, TermSerializer, ClassLevelSerializer, ClassRoomSerializer, SubjectSerializer, SubjectAllocationSerializer

# Create your views here.
class BaseAcademicViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['List', 'retrieve']:
            return [IsAuthenticated()]
        return [IsSchoolAdmin()]

class AcademicSessionViewSet(BaseAcademicViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer

class TermViewSet(BaseAcademicViewSet):
    queryset = Term.objects.select_related('session').all()
    serializer_class = TermSerializer

class ClassLevelViewSet(BaseAcademicViewSet):
    queryset = ClassLevel.objects.all()
    serializer_class = ClassLevelSerializer

class ClassRoomViewSet(BaseAcademicViewSet):
    queryset = ClassRoom.objects.select_related('level', 'form_teacher__user').all()
    serializer_class = ClassRoomSerializer

class SubjectViewSet(BaseAcademicViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectAllocationViewSet(BaseAcademicViewSet):
    queryset = SubjectAllocation.objects.select_related('teacher__user', 'subject', 'class_room__level', 'session').all()
    serializer_class = SubjectAllocationSerializer