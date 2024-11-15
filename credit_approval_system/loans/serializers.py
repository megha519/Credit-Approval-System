from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    Converts the Customer model instance into JSON and vice versa.
    """
    class Meta:
        model = Customer
        fields = '__all__'  # This will include all fields of the Customer model

class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model.
    Converts the Loan model instance into JSON and vice versa.
    """
    class Meta:
        model = Loan
        fields = '__all__'  # This will include all fields of the Loan model



