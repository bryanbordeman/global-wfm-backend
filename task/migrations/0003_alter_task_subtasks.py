# Generated by Django 4.0.4 on 2022-06-05 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_assignee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.ManyToManyField(null=True, to='task.subtask'),
        ),
    ]