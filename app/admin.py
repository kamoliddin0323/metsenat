from django.contrib import admin
from .models import Sponsor,University,Student, StudentSponsor

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('full_name','amount',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name','contract_amount','university',)

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name',)
   

@admin.register(StudentSponsor)
class StudentSponsorAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'student', 'amount',)