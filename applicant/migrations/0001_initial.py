# Generated by Django 3.1.7 on 2021-05-29 02:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curriculum_vitae', models.FileField(blank=True, null=True, upload_to='')),
                ('exp', models.CharField(blank=True, max_length=255, null=True)),
                ('skill', models.CharField(blank=True, max_length=255, null=True)),
                ('graduate', models.CharField(blank=True, max_length=255, null=True)),
                ('other', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]