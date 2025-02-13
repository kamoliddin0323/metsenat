from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework import permissions 
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import Sponsor, StudentSponsor,Student
from rest_framework import generics
from rest_framework.views import Response
from . import serializers
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from .permissions import Custompermission


class SponsorListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Sponsor.objects.all()
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('status', 'amount')
    search_fields = ['full_name', 'phone']
    authentication_classes = [TokenAuthentication,SessionAuthentication]


    def get_serializer_class(self):
        return serializers.SponsorSerializer if self.request.method == 'POST' else serializers.SponsorListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [Custompermission]
        return super().get_permissions()

class SponsorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListSerializer



class StudentSponsorCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StudentSponsorSerializer



class StudentSponsorUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorUpdateSerializer


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('type', 'university')
    search_fields = ['full_name']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    def get_serializer_class(self):
            return serializers.StudentSerializer if self.request.method == 'POST' else serializers.StudentListSerializer    



from django.db.models.functions import TruncMonth
from django.db.models import Count

class DashboardGraphAPIView(APIView):
    def get(self, request):
        this_year = timezone.now().year
        sponsors_data = (
            Sponsor.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')  
        )
        students_data = (
            Student.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        months = [entry['month'].strftime('%Y-%m') for entry in sponsors_data]
        sponsors_counts = [entry['count'] for entry in sponsors_data]
        students_counts = [entry['count'] for entry in students_data]

        data = {
            "months": months,
            "sponsors_counts": sponsors_counts,
            "students_counts": students_counts,
        }
        return Response(data=data)