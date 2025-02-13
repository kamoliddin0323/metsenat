from django.db import models

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sponsor(BaseModel):
    class SponsorType(models.TextChoices):
        LEGAL = 'legal', 'Yuridik'
        PERSONAL = 'personal', 'Jismoniy'
    
    class SponsorStatus(models.TextChoices):
        NEW = 'new', 'Yangi'
        MODERATION = 'moderation', 'Moderatsiya'
        APPROVED = 'approved', 'Tasdiqlangan'
        CANCELLED = 'cancelled', 'Bekor qilingan'
    
    class SponsorPaymentType(models.TextChoices):
        CASH = 'cash', 'Naqd'
        PLASTIC_CARD = 'plastic_card', 'Plastik karta'
        TRANSFER = 'transfer', 'Pul o\'tkazmasi'
    type  = models.CharField(
        max_length=20,
        choices=SponsorType.choices,default='personal'
    )
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13, null=True)
    amount = models.IntegerField()
    org_name = models.CharField(max_length=200, null=True)
    status = models.CharField(
        max_length=20, 
        choices=SponsorStatus.choices, 
        default=SponsorStatus.NEW
    )
    payment_type = models.CharField(
        max_length=50, 
        choices=SponsorPaymentType.choices,
        null=True
        )
    
    def __str__(self):
        return self.full_name
    

class University(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Student(BaseModel):
    class StudentType(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER = 'master', 'Magister'
    full_name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=200, 
        choices=StudentType.choices,default='bachelor'
    )
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    contract_amount = models.IntegerField(default=0)
    allocated_amount = models.IntegerField(default=0,null=True)
    phone = models.CharField(max_length=13)


    def __str__(self):
        return self.full_name


class StudentSponsor(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.sponsor.full_name} - {self.student.full_name}"
