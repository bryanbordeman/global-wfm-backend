# Generated by Django 4.0.4 on 2022-10-16 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0014_alter_contact_fax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='fax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contact.phone'),
        ),
    ]
