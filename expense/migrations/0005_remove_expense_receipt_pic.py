# Generated by Django 4.0.4 on 2022-06-19 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_expense_receipt_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='receipt_pic',
        ),
    ]