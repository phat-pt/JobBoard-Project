# Generated by Django 3.1.7 on 2021-06-05 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employer', '0003_auto_20210605_1022'),
        ('pages', '0026_auto_20210605_1022'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employer',
        ),
        migrations.AddField(
            model_name='employers',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]