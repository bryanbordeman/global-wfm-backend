from rest_framework import generics, permissions
from .serializers_expense import ExpenseSerializer, ExpenseApprovedSerializer
from expense.models import Expense as ExpenseModel

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
    serializer_class = ExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class ExpenseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseModel.objects.all()

class ExpenseToggleApproved(generics.UpdateAPIView):
    '''Approve expense. Admin view only'''
    serializer_class = ExpenseApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        # return WorkSegment.objects.filter(user=user)
        return ExpenseModel.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_approved=not(serializer.instance.is_approved)
        serializer.save()