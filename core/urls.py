from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sponsor/', views.SponsorListCreateAPIView.as_view()),
    path('sponsor/<int:pk>/', views.SponsorDetailAPIView.as_view()),
    path('sponsor-student/create/', views.StudentSponsorCreateAPIView.as_view()),
    path('sponsor-student/<int:pk>/', views.StudentSponsorUpdateAPIView.as_view()),
    path('student/', views.StudentListCreateAPIView.as_view()),
    path('graphs/', views.DashboardGraphAPIView.as_view())

]
