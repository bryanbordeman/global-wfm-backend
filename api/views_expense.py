from rest_framework import generics, permissions
from .serializers_expense import *
from expense.models import Expense as ExpenseModel
from expense.models import Mile as MileModel
from expense.models import MileRate as MileRatesModel
from django.contrib.auth.models import User
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.db import transaction

def filter_by_month(qs, month, year):
    qs_list = [i for i in qs]
    qs_filtered = []
    for i in qs_list:
        if i.date_purchased.month == month and i.date_purchased.year == year:
            qs_filtered.append(i)
    return qs_filtered

class Expense(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ExpenseSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #! need to add year to search
        month = self.kwargs['month']
        year = self.kwargs['year']
        user = self.request.user
        if user.is_staff:
            return filter_by_month(ExpenseModel.objects.all().order_by('-date_purchased'), month, year)
        else:
            return filter_by_month(ExpenseModel.objects.filter(user=user).order_by('-date_purchased'), month, year)

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

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # Set partial=True
        return super().get_serializer(*args, **kwargs)
    
    def perform_destroy(self, instance):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        file_field = instance.receipt_pic  # Retrieve the FieldFile object
        file_path = str(file_field)  # Convert the FieldFile object to a string (file path)

        try:
            s3.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path
            )
            with transaction.atomic():
                instance.delete()  # Delete the database instance

        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    
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
        month = self.kwargs['month']
        year = self.kwargs['year']
        user = self.request.user
        if user.is_staff:
            return filter_by_month(MileModel.objects.all().order_by('-date_purchased'), month, year)
        else:
            return filter_by_month(MileModel.objects.filter(user=user).order_by('-date_purchased'), month, year)

class MileToggleApproved(generics.UpdateAPIView):
    '''Approve expense. Admin view only'''
    serializer_class = MileApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MileModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_approved=not(serializer.instance.is_approved)
        serializer.save()

class MileCreate(generics.ListCreateAPIView):
    serializer_class = CreateMileSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MileModel.objects.all()
        else:
            return MileModel.objects.filter(user=user).order_by('-user')

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        serializer.save(user=user)

class MileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateMileSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MileModel.objects.all()

class MileRates(generics.ListAPIView):
    serializer_class = MileRatesSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MileRatesModel.objects.all()
