# Generated by Django 3.1.7 on 2021-06-05 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0006_employer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='user',
        ),
    ]
