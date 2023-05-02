from rest_framework import serializers
from .models import *


class ExpenseSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data related to expense.
    """

    class Meta:

        model = Expense
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data related to income.
    """

    class Meta:

        model = Income
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data related to transaction.
    """

    class Meta:

        model = Transaction
        fields = '__all__'
