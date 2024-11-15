
from email.feedparser import FeedParser

from django.shortcuts import render
from django.core.files.storage import default_storage
from .forms import UploadFileForm
from .models import Customer, Loan
from .tasks import process_loan_data, process_customer_data
from .serializers import CustomerSerializer, LoanSerializer

from rest_framework import status

# from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


class RegisterCustomerView(APIView):
    """
    Endpoint for registering a new customer.
    The customer will be assigned an approved limit based on their monthly income.
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            approved_limit = 36 * data['monthly_income']  # Example logic to calculate approved limit
            customer = Customer.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                monthly_income=data['monthly_income'],
                approved_limit=approved_limit,
                current_debt=0  # Assuming no debt initially
            )
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class CheckEligibilityView(APIView):
    """
    Endpoint to check if a customer is eligible for a loan.
    The eligibility check is based on a dummy credit score (can be enhanced with real logic).
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Dummy logic for eligibility (replace with real logic)
        credit_score = 70  # Dummy score for simplicity
        is_eligible = credit_score > 50

        response_data = {
            "customer_id": customer.id,
            "approval": is_eligible,
            "interest_rate": 8.5,  # Dummy interest rate (can be adjusted based on eligibility)
            "monthly_installment": 1500.00  # Example value for monthly installment
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CreateLoanView(APIView):
    """
    Endpoint to create a loan for a customer.
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the customer is eligible for the loan (dummy eligibility logic)
        if data['loan_amount'] > customer.approved_limit:
            return Response({"error": "Loan amount exceeds approved limit"}, status=status.HTTP_400_BAD_REQUEST)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data['loan_amount'],
            tenure=data['tenure'],
            interest_rate=data['interest_rate'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewLoanView(APIView):
    """
    Endpoint to view details of a specific loan.
    """
    def get(self, request, loan_id, *args, **kwargs):
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewLoansView(APIView):
    """
    Endpoint to view all loans for a specific customer.
    """
    def get(self, request, customer_id, *args, **kwargs):
        # Filter loans by customer_id
        loans = Loan.objects.filter(customer_id=customer_id)
        # Assuming you have a LoanSerializer
        from .serializers import LoanSerializer
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from .models import UploadedFile
from .tasks import process_loan_data, process_customer_data

def upload_loan_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()  # File saved to 'uploads/' directory
            file_path = file_instance.file.path  # Get the full file path
            process_loan_data.delay(file_path)  # Pass the path to the task
            return render(request, 'upload_success.html', {'file_type': 'Loan Data'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'file_type': 'Loan Data'})

def upload_customer_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            file_path = file_instance.file.path  # Get the full file path
            process_customer_data.delay(file_path)
            return render(request, 'upload_success.html', {'file_type': 'Customer Data'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'file_type': 'Customer Data'})


class UploadFileView(APIView):
    parser_classes = [MultiPartParser, FeedParser]

    def post(self, request, *args, **kwargs):
        try:
            # Check if file is in the request
            if 'file' not in request.FILES:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the uploaded file
            file = request.FILES['file']
            file_name = default_storage.save(file.name, file)
            file_path = default_storage.path(file_name)

            # Trigger the appropriate Celery task based on file name
            if 'loan' in file_name.lower():
                process_loan_data.delay(file_path)
                task_type = "Loan Data Processing"
            elif 'customer' in file_name.lower():
                process_customer_data.delay(file_path)
                task_type = "Customer Data Processing"
            else:
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": f"File '{file_name}' uploaded successfully.",
                "task": task_type,
                "file_path": file_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)