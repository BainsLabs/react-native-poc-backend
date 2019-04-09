# Generated by Django 2.2 on 2019-04-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('official_email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('image_url', models.URLField()),
            ],
        ),
    ]
