# Generated by Django 4.0.4 on 2022-12-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_hse_task_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
