from lender.models import Repayments
from django.forms import ModelForm
from django import forms


class RepaymentsForm(ModelForm):
    repaid_amount = forms.IntegerField(
        label='Total Repaid amount', help_text="Enter the total paid back amount for the reporting period.", widget=forms.TextInput(attrs={'autofocus': True}))
    PAR_30 = forms.IntegerField(
        label='Par 30 days', help_text="Enter the 30 day portfolio at risk for this month.\n If you don\'t have a PAR 30 value please fill in 0")
    PAR_60 = forms.IntegerField(
        label='Par 60 days', help_text="Enter the 60 day portfolio at risk for this month.\n If you don\'t have a PAR 60 value please fill in 0")
    PAR_90 = forms.IntegerField(
        label='Par 90 days', help_text="Enter the 90 day portfolio at risk for this month.\n If you don\'t have a PAR 90 value please fill in 0")
    PAR_over_90_days = forms.IntegerField(
        label='Par over 90 days', help_text="Enter the over 90 days portfolio at risk for this month.\n If you don\'t have a PAR over 90 days value please fill in 0")

    class Meta:
        model = Repayments
        fields = ("repaid_amount","PAR_30", "PAR_60",
                  "PAR_90", "PAR_over_90_days")
