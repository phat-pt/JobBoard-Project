# Generated by Django 3.1.7 on 2021-05-22 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_auto_20210522_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='flag',
            field=models.BooleanField(default=True, verbose_name=True),
            preserve_default=False,
        ),
    ]
