from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sponsor/', views.SponsorListCreateAPIView.as_view()),
    path('sponsor/<int:pk>/', views.SponsorDetailAPIView.as_view()),
    path('sponsor-student/create/', views.StudentSponsorCreateAPIView.as_view()),
    path('sponsor-student/<int:pk>/', views.StudentSponsorUpdateAPIView.as_view()),
    path('student/', views.StudentListCreateAPIView.as_view()),
    path('graphs/', views.DashboardGraphAPIView.as_view())

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    