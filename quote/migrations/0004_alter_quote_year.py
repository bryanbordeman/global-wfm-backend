# Generated by Django 4.0.4 on 2022-12-03 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0003_quote_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='year',
            field=models.CharField(editable=False, max_length=4, null=True),
        ),
    ]
