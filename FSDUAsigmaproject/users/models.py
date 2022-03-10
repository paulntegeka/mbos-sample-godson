from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(help_text="Enter a nine digit phone number. For example (789076068)",max_length=10,blank=False,null=False,validators=[RegexValidator(r'^\d{1,10}$')])

    class Meta:

        verbose_name = "program users (financial institution and staff users)"
        verbose_name_plural = "program users"
        
