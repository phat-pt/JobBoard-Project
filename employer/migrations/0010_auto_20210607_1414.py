# Generated by Django 3.1.7 on 2021-06-07 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0009_jobpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
