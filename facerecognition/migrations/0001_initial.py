# Generated by Django 2.2 on 2019-04-24 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image_url', models.URLField()),
                ('is_superuser', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('official_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.EmployeeDetails', to_field='official_email')),
            ],
        ),
    ]
