# Generated by Django 4.0.4 on 2022-05-31 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('worksegment', '0002_alter_worksegment_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksegment',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project.project'),
        ),
    ]
