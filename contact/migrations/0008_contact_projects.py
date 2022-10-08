# Generated by Django 4.0.4 on 2022-10-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_project_contact'),
        ('contact', '0007_contact_quotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='projects',
            field=models.ManyToManyField(blank=True, to='project.project'),
        ),
    ]