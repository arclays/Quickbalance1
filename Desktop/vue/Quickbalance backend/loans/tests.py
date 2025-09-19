from django.test import TestCase

# Create your tests here.
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

class LoanRenewal(models.Model):
    RENEWAL_TYPE_CHOICES = [
        ('full', 'Full Renewal - Same Terms'),
        ('partial', 'Partial Renewal - Adjusted Terms'),
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
    new_loan_term = models.PositiveIntegerField(help_text="Renewed loan term in months")
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
        """Calculate the new terms for the renewed loan"""
        # Get the current outstanding balance
        current_balance = self.loan.current_balance
        
        # Calculate any accrued interest up to renewal date
        accrued_interest = self._calculate_accrued_interest()
        
        # Set new principal to current balance + accrued interest + fees
        self.new_principal_amount = current_balance + accrued_interest + self.renewal_fee + self.processing_fee
        
        # Store the capitalized interest
        self.interest_capitalized = accrued_interest
        
        # Calculate total renewal amount
        self.total_renewal_amount = self.new_principal_amount
        
        # Set new due date (extend by the same term or new term)
        if self.renewal_type == 'full':
            self.new_due_date = self.renewal_date + timedelta(days=30 * self.previous_loan_term)
            self.new_loan_term = self.previous_loan_term
            self.new_interest_rate = self.previous_interest_rate
        else:
            # For partial or extended renewals, use the provided values
            self.new_due_date = self.renewal_date + timedelta(days=30 * self.new_loan_term)
    
    def _calculate_accrued_interest(self):
        """Calculate interest accrued from last payment to renewal date"""
        # Get the last payment date or loan start date
        last_payment = self.loan.repayments.order_by('-payment_date').first()
        start_date = last_payment.payment_date if last_payment else self.loan.start_date
        
        # Calculate days between last payment and renewal
        days_elapsed = (self.renewal_date - start_date).days
        
        # Calculate daily interest rate
        daily_rate = (self.loan.interest_rate / 100) / 365
        
        # Calculate accrued interest
        accrued_interest = self.loan.current_balance * daily_rate * days_elapsed
        
        return Decimal(accrued_interest).quantize(Decimal('0.01'))
    
    def save(self, *args, **kwargs):
        # Set previous loan state if not already set
        if not self.pk:
            self.previous_balance = self.loan.current_balance
            self.previous_interest_rate = self.loan.interest_rate
            self.previous_loan_term = self.loan.loan_term_months
            self.previous_due_date = self.loan.due_date
            
            # Calculate renewal terms
            self.calculate_renewal_terms()
        
        super().save(*args, **kwargs)
        
        # Charge renewal fees if applicable
        self._charge_renewal_fees()
        
        # Update the main loan with new terms if terms are accepted
        if self.terms_accepted:
            self._update_loan_terms()
    
    def _charge_renewal_fees(self):
        """Charge renewal and processing fees"""
        fees_to_charge = []
        
        if self.renewal_fee > 0:
            fees_to_charge.append(('renewal', self.renewal_fee, "Loan renewal fee"))
        
        if self.processing_fee > 0:
            fees_to_charge.append(('processing', self.processing_fee, "Renewal processing fee"))
        
        for fee_type, amount, description in fees_to_charge:
            LoanFeeCharge.objects.create(
                loan=self.loan,
                fee_type=fee_type,
                amount=amount,
                description=f"{description} for renewal on {self.renewal_date}"
            )
    
    def _update_loan_terms(self):
        """Update the main loan with the renewed terms"""
        self.loan.principal_amount = self.new_principal_amount
        self.loan.interest_rate = self.new_interest_rate
        self.loan.loan_term_months = self.new_loan_term
        self.loan.due_date = self.new_due_date
        self.loan.status = 'active'  # Reset status to active
        
        # Recalculate total loan amount
        self.loan.total_loan_amount = self.loan.calculate_total_loan_amount()
        self.loan.current_balance = self.loan.total_loan_amount
        
        # Reset repayment schedule
        self._create_new_repayment_schedule()
        
        self.loan.save()
    
    def _create_new_repayment_schedule(self):
        """Create a new repayment schedule for the renewed loan"""
        # Delete existing unpaid schedule items
        self.loan.repayment_schedule.filter(is_paid=False).delete()
        
        # Create new schedule based on repayment frequency
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
        """Get a summary of the renewal changes"""
        return {
            'previous_balance': self.previous_balance,
            'new_principal': self.new_principal_amount,
            'interest_capitalized': self.interest_capitalized,
            'fees_charged': self.renewal_fee + self.processing_fee,
            'previous_interest_rate': f"{self.previous_interest_rate}%",
            'new_interest_rate': f"{self.new_interest_rate}%",
            'previous_term': f"{self.previous_loan_term} months",
            'new_term': f"{self.new_loan_term} months",
            'previous_due_date': self.previous_due_date,
            'new_due_date': self.new_due_date,
        }