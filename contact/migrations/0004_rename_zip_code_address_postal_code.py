# Generated by Django 4.0.4 on 2022-09-04 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_address_place_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip_code',
            new_name='postal_code',
        ),
    ]