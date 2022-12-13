# Generated by Django 4.0.4 on 2022-12-10 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_alter_hse_created_alter_project_created_and_more'),
        ('task', '0002_alter_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='hse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.hse'),
        ),
        migrations.AddField(
            model_name='task',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.service'),
        ),
    ]