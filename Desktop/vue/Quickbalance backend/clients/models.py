from django.db import models
from django.conf import settings

class Client(models.Model):
    # Basic details
    first_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    # Identification
    national_id = models.CharField(max_length=50, unique=True, blank=True, null=True, default="N/A")
    passport_number = models.CharField(max_length=50, unique=True, blank=True, null=True, default="N/A")
    tin_number = models.CharField("Tax Identification Number", max_length=50, blank=True, null=True, default="N/A")
    # Employment / Occupation
    occupation = models.CharField(max_length=150, blank=True, null=True)
    employment_duration = models.CharField(max_length=50, blank=True, null=True)  # e.g., "2 years"
    # Business Information (if self-employed)
    business_name = models.CharField(max_length=200, blank=True, null=True, default="N/A")
    business_type = models.CharField(max_length=150, blank=True, null=True, default="N/A")
    business_registration_details = models.TextField(blank=True, null=True, default="N/A")
    # Contact
    phone = models.CharField(max_length=10, unique=True)
    other_phoneNos = models.CharField(max_length=20, unique=True, default="N/A")
    email = models.EmailField(blank=True, null=True, default="N/A")
    address = models.TextField(blank=True, null=True, default="N/A")

    # Credit officer assigned
    credit_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name="clients"
    )
    def save(self, *args, **kwargs):
        # Auto-generate full name
        self.full_name = f"{self.first_name} {self.other_names or ''}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

