# Generated by Django 4.0.4 on 2022-11-13 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_remove_ordertype_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='project.project')),
            ],
            bases=('project.project',),
        ),
    ]
