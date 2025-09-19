# serializers.py
from rest_framework import serializers
from .models import Client
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientSerializer(serializers.ModelSerializer):
    credit_officer_name = serializers.CharField(source='credit_officer.get_full_name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Client # fields = '__all__'
        fields = [
            'id',
            'first_name',
            'other_names',
            'full_name',
            'date_of_birth',
            'age',
            'gender',
            'marital_status',
            'national_id',
            'passport_number',
            'tin_number',
            'occupation',
            'employment_duration',
            'business_name',
            'business_type',
            'business_registration_details',
            'phone',
            'other_phoneNos',
            'email',
            'address',
            'credit_officer',
            'credit_officer_name'
        ]
        extra_kwargs = {
            'national_id': {'required': False},
            'passport_number': {'required': False},
            'tin_number': {'required': False},
            'other_phoneNos': {'required': False},
            'email': {'required': False},
            'address': {'required': False},
        }

    def validate_phone(self, value):
        # Validate phone number format
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits")
        return value

    def validate(self, data):
        # Validate that at least one identification is provided
        identifications = ['national_id', 'passport_number', 'tin_number']
        has_identification = any(data.get(field) and data.get(field) != "N/A" for field in identifications)
        
        if not has_identification:
            raise serializers.ValidationError(
                "At least one identification (National ID, Passport, or TIN) must be provided"
            )
        return data