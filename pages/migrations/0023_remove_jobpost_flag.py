# Generated by Django 3.1.7 on 2021-05-22 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_jobpost_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='flag',
        ),
    ]
