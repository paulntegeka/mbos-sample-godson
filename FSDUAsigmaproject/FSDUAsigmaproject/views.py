from distutils.log import error
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from codes.forms import CodeForm
from users.models import CustomUser
from .utils import send_verification_code
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.shortcuts import render
from lender.models import Disbursement, Repayments, ExpectedAmount, LenderOutstanding,Lender
from lender.resources import DisbursementResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from dateutil.relativedelta import relativedelta
from .forms import RepaymentsForm
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

import os
from django.http import HttpResponse, Http404


def download(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'lender-disbursment-template.xlsx'
    file_path = BASE_DIR + '/filedownloads/' + filename
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


class LandingView(TemplateView):
    template_name = "landing.html"


class Evaluation(LoginRequiredMixin, TemplateView):
    template_name = "evaluation.html"


@login_required
def home_view(request):
    form = RepaymentsForm(request.POST)

    if request.method == 'POST' and form.is_valid():
    
        disbursement_resource = DisbursementResource()
        dataset = Dataset()

        try:
            new_borrower = request.FILES['myfile']
        except MultiValueDictKeyError:
            form = RepaymentsForm()
            messages.info(
                request, 'The spreadsheet with fund disbursements has not been uploaded. Please Upload the spreadsheet for a successfull submission')
            return redirect('home-view')

        new_borrower = request.FILES['myfile']

        if not new_borrower.name.endswith('xlsx'):
            messages.info(
                request, 'Wrong file format. Please upload a spreadsheet.')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_borrower.read(), format='xlsx')

        right_colum_order = ['NIN', 'Phone_number', 'Borrower_ID', 'Loan_ID', 'Line_of_business', 'Gender', 'Age', 'Year_of_loan_issue', 'Month_of_loan_issue', 'Day_of_loan_issue', 'Year_of_repayments_commencement', 'Month_of_repayments_commencement', 'Day_of_repayments_commencement', 'Loan_amount',
                             'Tenure_of_loan', 'Interest_rate', 'Location_of_borrower', 'Expected_monthly_installment', 'Number_of_employees', ]

        if imported_data.headers != right_colum_order:
            messages.info(
                request, 'Colum headers in the uploaded spreadsheet are not as presented in shared template.')
            return render(request, 'upload.html', {'form': form})

        for data in imported_data:

            if type(data[0]) is str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the NIN column is not in the correct formart please check.')
                return redirect('home-view')

            if type(data[1]) is int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Phone_number column is not in the correct formart please ensure all phone numbers are in the form 0772123123.')
                return redirect('home-view')

            if type(data[2]) is int or str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Borrower_ID column is not in the correct formart please ensure all Borrower ID\'s are filled in.')
                return redirect('home-view')

            if type(data[3]) is int or str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Loan_ID column is not in the correct formart please ensure all Loan ID\'s are filled in.')
                return redirect('home-view')

            if type(data[4]) is str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Line_of_business column is not in the correct formart please ensure all line of business entries are filled in.')
                return redirect('home-view')

            if type(data[5]) is str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Gender column is not in the correct formart please ensure all line of gender are filled in. correct entries are either \'male\' or \'female\'')
                return redirect('home-view')

            if type(data[6]) is int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Age column is not in the correct formart please ensure all age entries are filled in, and are numbers')
                return redirect('home-view')

            if type(data[7]) is int and data[7] < 2030 and data[7] > 2021:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Year_of_loan_issue column is not in the correct formart please ensure all year entries are filled in, are numbers, and are between 2022 and 2027')
                return redirect('home-view')

            if type(data[8]) is int and data[8] < 13 and data[8] > 0:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Month_of_loan_issue column is not in the correct formart please ensure all month entries are filled in, are numbers, and are between 01 and 12')
                return redirect('home-view')

            if type(data[9]) is int and data[9] < 32 and data[8] > 0:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Day_of_loan_issue column is not in the correct formart please ensure all day entries are filled in, and are in the numerical')
                return redirect('home-view')

            ###############
            if type(data[10]) is int and data[10] < 2030 and data[10] > 2021:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Year_of_repayments_commencement column is not in the correct formart please ensure all year entries are filled in, are numbers, and are between 2022 and 2027')
                return redirect('home-view')

            if type(data[11]) is int and data[11] < 13 and data[11] > 0:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Month_of_repayments_commencement column is not in the correct formart please ensure all month entries are filled in, are numbers, and are between 01 and 12')
                return redirect('home-view')

            if type(data[12]) is int and data[12] < 32 and data[12] > 0:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Day_of_loan_issue column is not in the correct formart please ensure all day entries are filled in, and are in the numerical')
                return redirect('home-view')

            ##############

            if type(data[13]) is int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Loan_amount column is not in the correct formart please ensure all loan amount entries are filled in.')
                return redirect('home-view')

            if type(data[14]) is int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Tenure_of_loan column is not in the correct formart please ensure all tenure of loan entries are filled in, and are numbers')
                return redirect('home-view')

            if type(data[15]) is float or int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Interest_rate column is not in the correct formart please ensure all interest rate entries are filled in, and have at least one decimal place')
                return redirect('home-view')

            if type(data[16]) is str:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Location_of_borrower column is not in the correct formart please ensure all Location_of_borrower entries are filled in.')
                return redirect('home-view')

            if type(data[17]) is float or int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Expected_monthly_installment column is not in the correct formart please ensure all Expected_monthly_installment entries are filled in, and are numbers')
                return redirect('home-view')

            if type(data[18]) is int:
                pass
            else:
                messages.info(
                    request, 'At least one observation in the Number_of_employees column is not in the correct formart please ensure all Number_of_employees entries are filled in, and are numbers')
                return redirect('home-view')

            try:
                datetime.datetime(year=data[7], month=data[8], day=data[9])
            except ValueError:
                messages.info(
                    request, 'The dates on at least one of your observations are not correct. Please confirm their accuracy!')
                return redirect('home-view')

            try:
                datetime.datetime(year=data[10], month=data[11], day=data[12])
            except ValueError:
                messages.info(
                    request, 'The dates on at least one of your observations are not correct. Please confirm their accuracy!')
                return redirect('home-view')

        for data in imported_data:
            if Disbursement.objects.filter(unsubmission_gen_identfier=f'{data[0]}{data[3]}{request.user.Lenders.Institution_name}').exists():
                messages.info(
                    request, 'At least one duplicate entry has been detected in spreadsheet you are trying to upload ')
                return redirect('home-view')
            else:
                pass


        for data in imported_data:
            value = Disbursement()
            value.NIN = data[0]
            value.Phone_number = data[1]
            value.Borrower_ID = data[2]
            value.Loan_ID = data[3]
            value.Line_of_business = data[4]
            value.Gender = data[5]
            value.Age = data[6]
            value.Date_of_loan_issue = datetime.datetime(
                year=data[7], month=data[8], day=data[9])
            value.Date_of_repayments_commencement = datetime.datetime(
                year=data[10], month=data[11], day=data[12])
            value.Loan_amount = data[13]
            value.Tenure_of_loan = data[14]
            value.Interest_rate = data[15]
            value.Location_of_borrower = data[16]
            value.Expected_monthly_installment = data[17]
            value.Number_of_employees = data[18]
            value.lender = request.user.Lenders.Institution_name
            value.unsubmission_gen_identfier = f'{data[0]}{data[3]}{request.user.Lenders.Institution_name}'
            value.save()

        repayment = Repayments()
        repayment.PAR_30 = form.cleaned_data.get('PAR_30')
        repayment.PAR_60 = form.cleaned_data.get('PAR_60')
        repayment.PAR_90 = form.cleaned_data.get('PAR_90')
        repayment.PAR_over_90_days = form.cleaned_data.get('PAR_over_90_days')
        repayment.repaid_amount = form.cleaned_data.get('repaid_amount')
        repayment.lender = request.user.Lenders.Institution_name
        repayment.save()

        

        for data in imported_data:
            y = datetime.datetime(year=data[10], month=data[11], day=1)
            z = datetime.datetime(year=data[7], month=data[8], day=data[9])
            for i in range (data[14]):
                e_amounts = ExpectedAmount()
                e_amounts.lender = request.user.Lenders.Institution_name
                e_amounts.borrower_id = f'{data[0]}-{request.user.Lenders.Institution_name}-{data[3]}'
                e_amounts.Expected_monthly_installment = data[17]
                e_amounts.year = y.year
                e_amounts.month = y.month + i
                e_amounts.recent_object_filter = f'{request.user.Lenders.Institution_name}{y.year}{y.month}'
                e_amounts.save()

        l_outstanding = LenderOutstanding()
        l_outstanding.month = data[8]
        l_outstanding.year = data[7]

        if LenderOutstanding.objects.filter(lender=request.user.Lenders.Institution_name).first() is not None:
            l_outstanding.brought_foward_balance = LenderOutstanding.objects.filter(lender=request.user.Lenders.Institution_name).first().difference
        else:
            l_outstanding.brought_foward_balance = 0

        query = ExpectedAmount.objects.filter(year = z.year, month=z.month, lender=request.user.Lenders.Institution_name)
        q = 0
        for i in query:
            q+= i.Expected_monthly_installment

        l_outstanding.expected_amount = q + l_outstanding.brought_foward_balance

        l_outstanding.actual_amount_submitted = form.cleaned_data.get('repaid_amount')

        l_outstanding.difference = l_outstanding.expected_amount - l_outstanding.actual_amount_submitted
        

        l_outstanding.lender = request.user.Lenders.Institution_name

        l_outstanding.save()

        messages.info(request, 'Upload Successful')
        return redirect('home-view')

    form = RepaymentsForm()
    return render(request, 'upload.html', {'form': form})


def auth_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify-view')
        else:
            messages.error(
                request, f'Please check that the entered user name or password are as issued.')
            return redirect('login-view')
            # return redirect('login-view',{'form':form})

    return render(request, 'auth.html', {'form': form})


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    user = CustomUser.objects.get(pk=pk)
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username}:{user.code}"
        if not request.POST:
            send_verification_code(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                if user.is_staff:
                    return redirect('evaluation')
                else:
                    return redirect('home-view')
            else:
                messages.error(
                    request, f'Please ensure that the entered code matched the one in the sent sms')
                return redirect('login-view')
    return render(request, 'verify.html', {'form': form})
