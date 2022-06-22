from rest_framework import generics, permissions
from .serializers_expense import ExpenseSerializer, ExpenseApprovedSerializer, MileSerializer, CreateExpenseSerializer
from expense.models import Expense as ExpenseModel
from expense.models import Mile as MileModel
from django.contrib.auth.models import User

def filter_by_month(qs, month):
    qs_list = [i for i in qs]
    qs_filtered = []
    for i in qs_list:
        if i.date_purchased.month == month:
            qs_filtered.append(i)
    return qs_filtered

class Expense(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        month = self.kwargs['month']
        user = self.request.user
        if user.is_staff:
            return filter_by_month(ExpenseModel.objects.all(), month)
        else:
            return filter_by_month(ExpenseModel.objects.filter(user=user).order_by('-date_created'), month)

class ExpenseCreate(generics.ListCreateAPIView):
    serializer_class = CreateExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  
        user = self.request.user
        if user.is_staff:
            return ExpenseModel.objects.all()
        else:
            return ExpenseModel.objects.filter(user=user).order_by('-user')
    
    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        serializer.save(user=user)


class ExpenseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseModel.objects.all()

class ExpenseToggleApproved(generics.UpdateAPIView):
    '''Approve expense. Admin view only'''
    serializer_class = ExpenseApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseModel.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_approved=not(serializer.instance.is_approved)
        serializer.save()

class Mile(generics.ListAPIView):
    '''Employee view'''
    serializer_class = MileSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MileModel.objects.all()
