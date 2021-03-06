# Generated by Django 4.0.4 on 2022-06-25 10:46

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_expense_receipt_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='receipt_pic',
            field=imagekit.models.fields.ProcessedImageField(default='receipt.png', null=True, upload_to='None'),
        ),
    ]
