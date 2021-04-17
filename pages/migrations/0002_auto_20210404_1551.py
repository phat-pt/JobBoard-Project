# Generated by Django 3.1.7 on 2021-04-04 08:51

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobpost',
            old_name='CompanyName',
            new_name='company_name',
        ),
        migrations.RenameField(
            model_name='jobpost',
            old_name='CreatedDate',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='jobpost',
            old_name='IsActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='jobpost',
            old_name='JobLocation',
            new_name='job_apply_url',
        ),
        migrations.RenameField(
            model_name='jobpost',
            old_name='JobTitle',
            new_name='job_location',
        ),
        migrations.RemoveField(
            model_name='jobpost',
            name='JobDescription',
        ),
        migrations.RemoveField(
            model_name='jobpost',
            name='JobTypeID',
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_salary',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_summary',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='JobType',
        ),
    ]
