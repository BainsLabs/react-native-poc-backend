# Generated by Django 2.2 on 2019-04-09 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facerecognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('employee_id', models.CharField(max_length=100)),
                ('p_address', models.CharField(max_length=200)),
                ('c_address', models.CharField(max_length=200)),
                ('login_otp', models.CharField(max_length=100)),
                ('exp_otp', models.CharField(max_length=100)),
                ('official_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facerecognition.User', to_field='official_email')),
            ],
        ),
    ]