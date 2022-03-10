from django.contrib import admin
from .models import Disbursement,Lender,Repayments,FundingTranche,ExpectedAmount,LenderOutstanding
from import_export.admin import ImportExportModelAdmin
from import_export import resources

admin.site.site_url = "/evaluation/"
admin.site.site_header = "MSE Recovery Fund Monitoring Portal"
admin.site.site_title = "MSE Recovery Fund Monitoring Portal"
admin.site.index_title = "MSE Recovery Fund Monitoring Portal"



class DisbursementResource(resources.ModelResource):
    class Meta:
        model = Disbursement
        fields = ('id','lender','NIN', 'Phone_number','Borrower_ID','Loan_ID','Line_of_business','Gender','Age','Date_of_loan_issue','Date_of_repayments_commencement','Loan_amount','Tenure_of_loan','Interest_rate', 'Location_of_borrower', 'Expected_monthly_installment','Number_of_employees','created')
        export_order = ('id','lender','NIN', 'Phone_number','Borrower_ID','Loan_ID','Line_of_business','Gender','Age','Date_of_loan_issue','Date_of_repayments_commencement','Loan_amount','Tenure_of_loan','Interest_rate', 'Location_of_borrower', 'Expected_monthly_installment','Number_of_employees','created')
class DisbursementAdmin(ImportExportModelAdmin):
    list_filter = ('Date_of_loan_issue', 'Date_of_repayments_commencement','Line_of_business','lender','Gender',)
    list_display = ('lender','id', 'NIN', 'Phone_number','Borrower_ID','Line_of_business','Gender','Age','Date_of_loan_issue','Date_of_repayments_commencement','Loan_amount')
    resource_class = DisbursementResource

admin.site.register(Disbursement, DisbursementAdmin)




class FundingTrancheResource(resources.ModelResource):
    class Meta:
        model = FundingTranche
        fields = ('lender','id', 'sent_amount', 'date_sent')
        export_order = ('lender','id', 'sent_amount', 'date_sent')

class FundingTrancheAdmin(ImportExportModelAdmin):
    list_filter = ('date_sent','lender',)
    list_display = ('lender','id', 'sent_amount', 'date_sent')
    resource_class = FundingTrancheResource

admin.site.register(FundingTranche, FundingTrancheAdmin)





class RepaymentsResource(resources.ModelResource):
    class Meta:
        model = Repayments
        fields = ('lender','id','repaid_amount','PAR_30','PAR_60','PAR_90','PAR_over_90_days','date_sent','repaid_amount',)
        export_order = ('lender','id','repaid_amount','PAR_30','PAR_60','PAR_90','PAR_over_90_days','date_sent',)

class RepaymentsAdmin(ImportExportModelAdmin):
    list_filter = ('lender','date_sent',)
    list_display = ('lender','id','repaid_amount','PAR_30','PAR_60','PAR_90','PAR_over_90_days','date_sent',)
    resource_class = RepaymentsResource

admin.site.register(Repayments, RepaymentsAdmin)







class LenderResource(resources.ModelResource):
    class Meta:
        model = Lender
        fields = ('id', 'Institution_name', 'Institution_tier',)
        export_order = ('id', 'Institution_name', 'Institution_tier',)

class LenderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'Institution_name', 'Institution_tier','Lender_contact_person','active_lender')
    resource_class = LenderResource

admin.site.register(Lender,LenderAdmin)





####
class ExpectedAmountResource(resources.ModelResource):
    class Meta:
        model = FundingTranche
        fields = ('borrower_id','lender','Expected_monthly_installment', 'year','month')
        export_order = ('borrower_id','lender','Expected_monthly_installment', 'year','month')

class ExpectedAmountAdmin(ImportExportModelAdmin):
    search_fields=('borrower_id',)
    list_filter = ('lender',)
    list_display = ('borrower_id','lender','Expected_monthly_installment', 'year','month')
    resource_class = ExpectedAmountResource
admin.site.register(ExpectedAmount,ExpectedAmountAdmin)


####
class LenderOutstandingResource(resources.ModelResource):
    class Meta:
        model = LenderOutstanding
        fields = ('lender','year','month','difference','brought_foward_balance','expected_amount','actual_amount_submitted',)
        export_order = ('lender','year','month','difference','brought_foward_balance','expected_amount','actual_amount_submitted',)

class LenderOutstandingAdmin(ImportExportModelAdmin):
    search_fields=('lender','year','month')
    list_filter = ('lender',)
    list_display = ('lender','year','month','difference','brought_foward_balance','expected_amount','actual_amount_submitted',)
    resource_class = LenderOutstandingResource
admin.site.register(LenderOutstanding,LenderOutstandingAdmin)




