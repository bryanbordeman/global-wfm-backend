# Generated by Django 4.0.4 on 2022-06-18 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_remove_expense_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='_month_purchased',
            field=models.IntegerField(null=True),
        ),
    ]
