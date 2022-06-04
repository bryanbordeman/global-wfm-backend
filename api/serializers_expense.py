from rest_framework import serializers
from expense.models import Expense

class  ExpenseSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = Expense
        fields = ['id']
        read_only_fields = ['project', 'receipt_pic', 'merchant', 'price', 'notes', 'is_reimbursable', 'is_approved', 'date_purchased', 'date_created']