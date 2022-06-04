# Generated by Django 4.0.4 on 2022-06-04 10:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import expense.models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MileRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(null=True)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Mile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miles', models.FloatField(null=True)),
                ('notes', models.TextField(blank=True, max_length=250, validators=[django.core.validators.MaxLengthValidator(250)])),
                ('is_approved', models.BooleanField(default=False)),
                ('date', models.DateField(null=True, validators=[expense.models.no_future])),
                ('date_created', models.DateField(auto_now_add=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('rate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='expense.milerate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_pic', imagekit.models.fields.ProcessedImageField(default='receipt.png', upload_to='receipt_pic')),
                ('merchant', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(null=True)),
                ('notes', models.TextField(blank=True, max_length=250, validators=[django.core.validators.MaxLengthValidator(250)])),
                ('is_reimbursable', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('date_purchased', models.DateField(null=True, validators=[expense.models.no_future])),
                ('date_created', models.DateField(auto_now_add=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
