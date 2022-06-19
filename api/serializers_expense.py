from rest_framework import serializers
from expense.models import Expense, Mile

class  ExpenseSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = Expense
        fields = '__all__'
        depth = 1

class  CreateExpenseSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    is_approved = serializers.ReadOnlyField()
    # receipt_pic = serializers.ImageField() 
    class Meta:
        model = Expense
        # fields = '__all__'
        exclude = ['user']


class ExpenseApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = Expense
        fields = ['id']
        read_only_fields = ['project', 'receipt_pic', 'merchant', 'price', 'notes', 'is_reimbursable', 'is_approved', 'date_purchased', 'date_created']

class  MileSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    class Meta:
        model = Mile
        fields = '__all__'
        depth = 1
