from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from clients.models import Client
from datetime import timedelta

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('mortgage', 'Mortgage'),
        ('school_fees', 'School Fees Loan'),
        ('emergency', 'Emergency loan'),
        ('other', 'Other'),
    ]

    REPAYMENT_FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
         ('Renewal', 'Renewal'),
        ('active', 'Active'),
        ('delinquent', 'Delinquent'),
        ('restructured', 'Restructured'),
        ('closed', 'Closed'),
        ('defaulted', 'Defaulted'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="loans")
    
    # Loan details
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)
    principal_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Original loan amount before fees/interest"
    )
    loan_purpose = models.TextField(blank=True)
    loan_terms = models.PositiveIntegerField(help_text="Loan term period")
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="percentage rate (%)",
        validators=[MinValueValidator(0)]
    )
    repayment_frequency = models.CharField(max_length=20, choices=REPAYMENT_FREQUENCY_CHOICES)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='pending')

    # Fees and charges
    processing_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    insurance_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    other_fees = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    # Calculated amounts (updated after each transaction)
    total_loan_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        help_text="Principal + interest"
    )
    total_fees_charged = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    total_interest_charged = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    total_fines_charged = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    total_amount_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    current_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )

    # Collateral (optional)
    collateral_description = models.TextField(blank=True, help_text="Description of collateral provided")
    collateral_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Estimated value of collateral"
    )

    # Guarantor (optional)
    guarantor_name = models.CharField(max_length=200, blank=True)
    guarantor_contact = models.CharField(max_length=50, blank=True)
    guarantor_id_ref = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="ID number or reference for guarantor"
    )
    # Dates
    application_date = models.DateField(default=timezone.now)
    approval_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.client.full_name} - {self.loan_type} Loan (${self.principal_amount})"

    def calculate_total_loan_amount(self):
        interest_amount = (self.principal_amount * (self.interest_rate /  100))
        total_fees = self.processing_fee + self.insurance_fee + self.other_fees
        
        return self.principal_amount + interest_amount  , total_fees

    def update_loan_balances(self):
        """Update all calculated balances based on transactions"""
        # Get all related transactions
        disbursements = self.disbursements.aggregate(total=models.Sum('amount'))['total'] or 0
        repayments = self.repayments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
        fees = self.fee_charges.aggregate(total=models.Sum('amount'))['total'] or 0
        fines = self.fine_charges.aggregate(total=models.Sum('amount'))['total'] or 0
        
        # Update fields
        self.total_fees_charged = fees
        self.total_fines_charged = fines
        self.total_amount_paid = repayments
        self.current_balance = self.total_loan_amount - repayments
        
        self.save(update_fields=[
            'total_fees_charged', 
            'total_fines_charged', 
            'total_amount_paid', 
            'current_balance'
        ])

    def save(self, *args, **kwargs):
        # Calculate total loan amount if not set
        if not self.total_loan_amount or self.pk is None:
            self.total_loan_amount = self.calculate_total_loan_amount()
            self.current_balance = self.total_loan_amount
            
        super().save(*args, **kwargs)


class LoanFeeCharge(models.Model):
    FEE_TYPE_CHOICES = [
        ('processing', 'Processing Fee'),
        ('insurance', 'Insurance Fee'),
        ('service', 'Service Fee'),
        ('other', 'Other Fee'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="fee_charges")
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    charge_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update loan balances after fee charge
        self.loan.update_loan_balances()
    
    def __str__(self):
        return f"{self.fee_type} fee of ${self.amount} for Loan #{self.loan.id}"


class LoanFineCharge(models.Model):
    FINE_TYPE_CHOICES = [
        ('late_payment', 'Late Payment Fine'),
        ('default', 'Default Fine'),
        ('other', 'Other Fine'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="fine_charges")
    fine_type = models.CharField(max_length=20, choices=FINE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    charge_date = models.DateField(default=timezone.now)
    reason = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update loan balances after fine charge
        self.loan.update_loan_balances()
    
    def __str__(self):
        return f"{self.fine_type} fine of ${self.amount} for Loan #{self.loan.id}"


class LoanRepaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="repayment_schedule")
    due_date = models.DateField()
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2)
    fees_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['due_date']

    def save(self, *args, **kwargs):
        # Calculate total amount due
        if not self.total_amount_due:
            self.total_amount_due = self.principal_amount + self.interest_amount + self.fees_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment due {self.due_date} for Loan #{self.loan.id}"

    def update_payment_status(self):
        """Update is_paid status based on actual payments"""
        total_paid = self.payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
        self.is_paid = total_paid >= self.total_amount_due
        self.save()


class LoanRepayment(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('MOMO', ' MOMO Cash'),
        ('bank', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]

    PAYMENT_ALLOCATION_CHOICES = [
        ('principal', 'Principal'),
        ('interest', 'Interest'),
        ('fees', 'Fees'),
        ('fines', 'Fines'),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name="repayments")
    schedule = models.ForeignKey(
        LoanRepaymentSchedule,
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name="payments"
    )
    payment_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    receipt_number = models.CharField(max_length=50, blank=True, help_text="Payment receipt reference")
    
    # Payment allocation breakdown
    principal_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    interest_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    fees_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    fines_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    # Late payment tracking
    is_late = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Any notes about this payment")

    def save(self, *args, **kwargs):
        if self.schedule and self.payment_date > self.schedule.due_date:
            self.is_late = True
        allocation_total = self.principal_paid + self.interest_paid + self.fees_paid + self.fines_paid
        if allocation_total != self.amount_paid:
            remaining = self.amount_paid
            if remaining > 0 and self.loan.total_fines_charged > self.loan.fine_charges.aggregate(
                paid=models.Sum('repayments__fines_paid'))['paid'] or 0:
                self.fines_paid = min(remaining, self.loan.total_fines_charged - 
                                     (self.loan.fine_charges.aggregate(paid=models.Sum('repayments__fines_paid'))['paid'] or 0))
                remaining -= self.fines_paid
            if remaining > 0 and self.loan.total_fees_charged > self.loan.fee_charges.aggregate(
                paid=models.Sum('repayments__fees_paid'))['paid'] or 0:
                self.fees_paid = min(remaining, self.loan.total_fees_charged - 
                                    (self.loan.fee_charges.aggregate(paid=models.Sum('repayments__fees_paid'))['paid'] or 0))
                remaining -= self.fees_paid
            if remaining > 0 and self.loan.total_interest_charged > self.loan.repayments.aggregate(
                paid=models.Sum('interest_paid'))['paid'] or 0:
                self.interest_paid = min(remaining, self.loan.total_interest_charged - 
                                        (self.loan.repayments.aggregate(paid=models.Sum('interest_paid'))['paid'] or 0))
                remaining -= self.interest_paid
            self.principal_paid = remaining
        
        super().save(*args, **kwargs)
        
        # Update schedule payment status
        if self.schedule:
            self.schedule.update_payment_status()
        
        # Update loan balances
        self.loan.update_loan_balances()

    def __str__(self):
        return f"Payment of ${self.amount_paid} for Loan #{self.loan.id} on {self.payment_date}"

class LoanClosure(models.Model):
    SETTLEMENT_TYPE_CHOICES = [
        ('full', 'Full Settlement'),
        ('partial', 'Partial Settlement'),
        ('write_off', 'Write Off'),
    ]

    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name="closure")
    closure_date = models.DateField(default=timezone.now)
    settlement_type = models.CharField(max_length=20, choices=SETTLEMENT_TYPE_CHOICES)
    final_settlement_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    notes = models.TextField(blank=True, help_text="Closure notes or comments")

    def save(self, *args, **kwargs):
        # Update loan status when closed
        self.loan.status = 'closed'
        self.loan.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan #{self.loan.id} closed on {self.closure_date}"
    
    
class LoanRenewal(models.Model):
    RENEWAL_TYPE_CHOICES = [
        ('full', 'Full Renewal'),
        ('partial', 'Partial Renewal'),
        ('extended', 'Extended Term Only'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="renewals")
    renewal_date = models.DateField(default=timezone.now)
    renewal_type = models.CharField(max_length=20, choices=RENEWAL_TYPE_CHOICES, default='full')
    # New terms after renewal
    new_principal_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Principal amount for renewed loan (usually the outstanding balance)"
    )
    new_interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Interest rate for renewed loan period"
    )
    new_loan_term = models.PositiveIntegerField(help_text="Renewed loan term period")
    new_due_date = models.DateField(help_text="New due date after renewal")
    reason = models.TextField(help_text="Reason for renewal")
    terms_accepted = models.BooleanField(default=False, help_text="Client has accepted new terms")
     
    class Meta:
        ordering = ['-renewal_date']
        verbose_name = "Loan Renewal"
        verbose_name_plural = "Loan Renewals"
    
    def __str__(self):
        return f"Renewal #{self.id} for Loan #{self.loan.id} on {self.renewal_date}"
    
    def calculate_renewal_terms(self):
        current_balance = self.loan.current_balance
        new_interest_rate = self.loan.interest_rate
        self.new_principal_amount = current_balance 
        self.total_renewal_amount = self.new_principal_amount + new_interest_rate

        # Set new due date (extend by the same term or new term)
        if self.renewal_type == 'full':
            self.new_due_date = self.renewal_date + timedelta(days=self.loan.loan_terms)
            self.new_loan_terms = self.loan.loan_terms
            self.new_interest_rate = self.loan.interest_rate
        else:
            # For partial or extended renewals, use the provided values
            self.new_due_date = self.renewal_date + timedelta(days=self.new_loan_term)
        
        # Update the main loan with new terms if terms are accepted
        if self.terms_accepted:
            self._update_loan_terms()
    
    def _update_loan_terms(self):
        """Update the main loan with the renewed terms"""
        self.loan.current_balance = self.new_principal_amount
        self.loan.interest_rate = self.new_interest_rate
        self.loan.loan_terms = self.new_loan_terms
        self.loan.due_date = self.new_due_date
        self.loan.status = 'Renewal'  # Reset status to Renewal
        # Recalculate total loan amount
        self.loan.total_loan_amount = self.loan.calculate_total_loan_amount()
        self.loan.current_balance = self.loan.total_loan_amount
        
        # Reset repayment schedule
        self._create_new_repayment_schedule()
        
        self.loan.save()
    
    def _create_new_repayment_schedule(self):
        """Create a new repayment schedule for the renewed loan"""
        self.loan.repayment_schedule.filter(is_paid=False).delete()
        monthly_payment = self.new_principal_amount / self.new_loan_term
        
        for i in range(self.new_loan_term):
            due_date = self.renewal_date + timedelta(days=30 * (i + 1))
            
            LoanRepaymentSchedule.objects.create(
                loan=self.loan,
                due_date=due_date,
                principal_amount=monthly_payment,
                interest_amount=0,  # Would need interest calculation logic
                total_amount_due=monthly_payment,
                is_paid=False
            )
    
    def get_renewal_summary(self):
        return {
            'new_principal': self.new_principal_amount,
            'new_interest_rate': f"{self.new_interest_rate}%",
            'new_term': f"{self.new_loan_term} months",
            'new_due_date': self.new_due_date,
        }