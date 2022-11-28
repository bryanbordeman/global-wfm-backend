# Generated by Django 4.0.4 on 2022-11-28 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_initial'),
        ('project', '0003_project_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='hse',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='contact.company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='contact.company'),
            preserve_default=False,
        ),
    ]
