from django.urls import path
from .views import RegisterCustomerView, CheckEligibilityView, CreateLoanView, UploadFileView, ViewLoanView, ViewLoansView,UploadedFile

urlpatterns = [
    # Endpoint to register a new customer
    path('register/', RegisterCustomerView.as_view(), name='register_customer'),
    
    # Endpoint to check loan eligibility for a customer
    path('check-eligibility/', CheckEligibilityView.as_view(), name='check_eligibility'),
    
    # Endpoint to create a loan for a customer
    path('create-loan/', CreateLoanView.as_view(), name='create_loan'),
    
    # Endpoint to view a specific loan based on loan ID
    path('view-loan/<int:id>/', ViewLoanView.as_view(), name='view_loan'),
    
    # Endpoint to view all loans for a customer
    path('view-loans/<int:customer_id>/', ViewLoansView.as_view(), name='view_loans'),
    path('upload/', UploadFileView.as_view(), name='file-upload')
]
