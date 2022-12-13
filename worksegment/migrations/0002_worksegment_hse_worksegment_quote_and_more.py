# Generated by Django 4.0.4 on 2022-12-13 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0006_alter_quote_created'),
        ('project', '0007_alter_hse_created_alter_project_created_and_more'),
        ('worksegment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksegment',
            name='hse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project.hse'),
        ),
        migrations.AddField(
            model_name='worksegment',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='quote.quote'),
        ),
        migrations.AddField(
            model_name='worksegment',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project.service'),
        ),
    ]