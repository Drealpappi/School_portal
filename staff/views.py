from django.shortcuts import render
from core.permissions import IsSchoolAdmin, IsTeacherOrAdmin
from rest_framework import viewsets
from .models import StaffProfile
from .serializers import StaffProfileReadSerializer, StaffCreateSerializer

# Create your views here.
class StaffViewSet(viewsets.ModelviewSet):
    queryset = StaffProfile.objects.select_related('user').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsTeacherOrAdmin()]

        return [IsSchoolAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return StaffCreateSerializer
        return StaffProfileReadSerializer