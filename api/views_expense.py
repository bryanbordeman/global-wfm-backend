from rest_framework import generics, permissions
from .serializers_expense import ExpenseSerializer, ExpenseApprovedSerializer
from expense.models import Expense as ExpenseModel

class Expense(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ExpenseModel.objects.all()
        else:
            return ExpenseModel.objects.filter(user=user).order_by('-created')

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