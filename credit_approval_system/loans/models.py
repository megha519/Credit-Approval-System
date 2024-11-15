from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)

    monthly_income = models.IntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.FloatField()
    tenure = models.IntegerField()  # in months
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    em_paid_on_time = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan for {self.customer.first_name} {self.customer.last_name}"

    def calculate_monthly_installment(self):
        """
        Calculate the monthly installment based on loan amount, interest rate, and tenure.
        This is a simplified method and can be enhanced with more complex logic.
        """
        # Example formula for monthly installment calculation
        principal = self.loan_amount
        rate = self.interest_rate / 100 / 12  # monthly interest rate
        months = self.tenure
        
        if rate > 0:
            installment = (principal * rate) / (1 - (1 + rate) ** -months)
        else:
            installment = principal / months

        return round(installment, 2)

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate the monthly installment 
        when a loan is created or updated.
        """
        self.monthly_installment = self.calculate_monthly_installment()
        super().save(*args, **kwargs)
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
