# Generated by Django 3.1.7 on 2021-06-05 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0026_auto_20210605_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobpost',
            old_name='Recruiter',
            new_name='Employers',
        ),
    ]
