# Generated by Django 3.1.7 on 2021-04-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20210417_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='job_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
