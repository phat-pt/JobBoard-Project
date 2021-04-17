# Generated by Django 3.1.7 on 2021-04-14 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20210404_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('ID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('applicant_name', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.BinaryField(verbose_name=1)),
                ('email_address', models.CharField(blank=True, max_length=200, null=True)),
                ('file_upload', models.FileField(upload_to='')),
                ('user_name', models.CharField(blank=True, max_length=200, null=True)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('account_status', models.BooleanField(verbose_name=False)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationDetail',
            fields=[
                ('ID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('application_status', models.BooleanField(verbose_name=False)),
                ('applicant_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_address', models.CharField(blank=True, max_length=200, null=True)),
                ('company_email', models.CharField(blank=True, max_length=200, null=True)),
                ('company_website', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('account_status', models.BooleanField(verbose_name=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='jobpost',
            name='company_name',
        ),
        migrations.DeleteModel(
            name='JobPostSkillSet',
        ),
        migrations.DeleteModel(
            name='SkillSet',
        ),
        migrations.AddField(
            model_name='applicationdetail',
            name='job_post_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.jobpost'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.company'),
        ),
    ]