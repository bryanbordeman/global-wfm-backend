# Generated by Django 4.0.4 on 2022-05-31 08:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0003_alter_announcement_is_active_alter_announcement_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='memo',
            field=models.TextField(blank=True, max_length=1000, validators=[django.core.validators.MaxLengthValidator(1000)]),
        ),
    ]
