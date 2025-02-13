from rest_framework import serializers
from .import models
from django.contrib.auth.models import User
from django.db.models import Sum


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = ('full_name','phone','amount', 'org_name', 'type')

    # post, putch, put
    def validate(self, attrs):
        type = attrs.get('type')
        org_name = attrs.get('org_name')
        if type == 'personal' and org_name:
            raise serializers.ValidationError({
                'error': "Jismoniy shahslar uchun organizatsiya nomi kiritish mumkin emas"
            }, code=400)

        if type == 'legal' and not org_name:
            raise serializers.ValidationError({
                'error': "Yuridik  shahslar uchun organizatsiya nomi kiritish majburiy"
            }, code=400)
        return super().validate(attrs)


class SponsorListSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()

    class Meta:
        model = models.Sponsor
        exclude = ('org_name','payment_type')

    def get_spent_amount(self,obj):
        return obj.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0

class StudentSponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = "__all__"

    def validate(self, attrs):
        student = attrs.get('student')
        sponsor = attrs.get('sponsor')
        amount = attrs.get('amount')

        # studentga ortiqcha pul berish holati 
        student_received_money = student.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0
        diff = student.contract_amount - student_received_money
        if diff < amount:
            raise serializers.ValidationError({
                'error': f"Bu ta'labaga maksimal miqdorda {diff} so'm pul ajrata olasiz"
            })

        # va sponsorda pul yetishmasligi
        sponsor_spent_money = sponsor.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0
        diff = sponsor.amount - sponsor_spent_money 
        if diff < amount:
            raise serializers.ValidationError({
                'error': f"Bu homiyada {diff} so'm miqdorida pul qo'lgan"
            })
        return super().validate(attrs)



class StudentSponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = ("sponsor", 'amount')

    def update(self, instance, validated_data):
        student = instance.student
        student_total_received = student.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0
        
        if "amount" in validated_data and "sponsor" in validated_data: 
            if validated_data['sponsor'] == instance.sponsor and validated_data['amount'] != instance.amount:
                sponsor_amount = instance.sponsor.amount
                allocated_amount = instance.sponsor.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0 - instance.amount
                if sponsor_amount - allocated_amount < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {sponsor_amount - allocated_amount} so'm qoldiq mavjud"
                    })
                if student.contract_amount - student_total_received - instance.amount < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu talabaga {student.contract_amount - student_total_received - instance.amount} so'm berish mumkin"
                    })
                
            elif validated_data['sponsor'] != instance.sponsor and validated_data['amount'] == instance.amount:
                sponsor = validated_data['sponsor']
                sponsor_spent_amount = sponsor.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0
                if sponsor.amount - sponsor_spent_amount < instance.amount:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {sponsor.amount - sponsor_spent_amount} so'm  mavjud"
                    })
            elif validated_data['sponsor'] != instance.sponsor and validated_data['amount'] != instance.amount:
                sponsor = validated_data['sponsor']
                sponsor_spent_money = sponsor.studentsponsor_set.aggregate(total=Sum('amount'))['total'] or 0

                if sponsor.amount - sponsor_spent_money < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {sponsor.amount - sponsor_spent_money} so'm  mavjud"
                    })
                
                if student.contract_amount - (student_total_received - instance.amount) < validated_data['amount'] :
                    raise serializers.ValidationError({
                        'error': f"Bu talabaga {student.contract_amount - (student_total_received - instance.amount)} so'm  berish mumkin"
                    })

        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = '__all__'

    def validate(self, attrs):
        phone_number = attrs.get('phone')
        if phone_number and str(phone_number)[0:4] != '+998':
            raise serializers.ValidationError(detail={
                'error': 'Telefon raqamni tekshirib qaytadan kiriting'
            },code=401)
        return super().validate(attrs)

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'
    
    def validate(self, attrs):
        return super().validate(attrs)

