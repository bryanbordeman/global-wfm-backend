# Generated by Django 4.0.4 on 2022-12-03 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_quote_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='year',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
