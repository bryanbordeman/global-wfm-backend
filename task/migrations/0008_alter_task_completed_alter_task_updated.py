# Generated by Django 4.0.4 on 2022-06-07 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_alter_task_completed_alter_task_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
    ]
