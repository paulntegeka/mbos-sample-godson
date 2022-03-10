from import_export import resources
from .models import Disbursement

class DisbursementResource(resources.ModelResource):
    class meta:
        model = Disbursement
