from operator import mod
import re
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.forms import ValidationError

TIER_LEVEL = (
    ('3', 'Tier III'),
    ('4', 'Tier IV - MFI'),
    ('5', 'Tier IV - SACCOS'),
)
class Lender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Institution_name = models.CharField(max_length=25)
    Institution_tier = models.CharField(max_length=1,choices=TIER_LEVEL,blank=False,)
    active_lender = models.BooleanField(default=True)
    Lender_contact_person = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='Lenders')

    class Meta:
        verbose_name_plural = "lenders"

        verbose_name = "lender (financial institution)"
        verbose_name_plural = "lenders (financial institution)"

    def __str__(self):
        return self.Institution_name

class FundingTranche(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sent_amount = models.DecimalField(max_digits=13,decimal_places=2)
    date_sent = models.DateTimeField()
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE, db_column='Institution_name')
    related_query_name="tag"

    class Meta:
        ordering = ('-date_sent',)
        verbose_name_plural = "funding tranches"

    def __str__(self):
        return f'{self.lender.Institution_name} tranche id {self.id}'


class Disbursement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    NIN = models.CharField(max_length=25,null=False)
    Phone_number = models.IntegerField()
    Borrower_ID = models.TextField(max_length=25,null=False)
    Loan_ID = models.TextField(max_length=25,null=False)
    Line_of_business = models.CharField(
        max_length=25,
    )
    Gender = models.CharField(
        max_length=25,
    )
    Age = models.IntegerField()
    Date_of_loan_issue = models.DateField()
    Date_of_repayments_commencement = models.DateField()
    Loan_amount = models.IntegerField()
    Tenure_of_loan = models.PositiveIntegerField()
    Interest_rate = models.DecimalField(max_digits=125, decimal_places=2)
    Location_of_borrower = models.CharField(max_length=25)
    Expected_monthly_installment = models.IntegerField()
    Number_of_employees = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lender = models.CharField(max_length=25)
    unsubmission_gen_identfier = models.CharField(max_length=255,)


    class Meta:
        ordering = ('-created',)
        verbose_name = "disbursement"
        verbose_name_plural = "disbursements"

    def __str__(self):
        return self.Borrower_ID

class ExpectedAmount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lender =  models.CharField(max_length=255)
    borrower_id = models.CharField(max_length=255)
    Expected_monthly_installment = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    recent_object_filter = models.CharField(max_length=255)

    class Meta:
        ordering = ('lender','year','month')
        verbose_name_plural = "Expected Amounts"

    def __str__(self):
        return f'{self.lender} - expected amount id - {self.id} '


class LenderOutstanding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.IntegerField()
    year = models.IntegerField()
    difference = models.IntegerField()
    brought_foward_balance = models.IntegerField(default=0)
    expected_amount = models.IntegerField()
    actual_amount_submitted = models.IntegerField()
    lender = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "Lender Outstanding Amounts"

    def __str__(self):
        return f'{self.lender} - outstanding amount id - {self.id} '


class Repayments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lender = models.CharField(max_length=25)
    PAR_30 = models.IntegerField(help_text="Enter the 30 day portfolio at risk for this month.")
    PAR_60 = models.IntegerField(help_text="Enter the 60 day portfolio at risk for this month.")
    PAR_90 = models.IntegerField(help_text="Enter the 90 day portfolio at risk for this month.")
    PAR_over_90_days = models.IntegerField(help_text="Enter the over 90 days portfolio at risk for this month.") 
    date_sent = models.DateTimeField(auto_now_add=True)
    repaid_amount = models.IntegerField(help_text="Enter the total repaid amount for this month.")

    class Meta:
        ordering = ('-date_sent',)
        verbose_name = "Repayment"
        verbose_name_plural = "Repayments"

    def __str__(self):
        return self.lender


