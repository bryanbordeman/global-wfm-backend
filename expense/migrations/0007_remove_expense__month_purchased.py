# Generated by Django 4.0.4 on 2022-06-18 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_expense__month_purchased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='_month_purchased',
        ),
    ]
