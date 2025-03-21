# Generated by Django 4.0.5 on 2025-03-08 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_additionalrequirement_benifit_educationalrequirement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='additional_requirements',
            field=models.ManyToManyField(blank=True, to='page.additionalrequirement'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='benifits',
            field=models.ManyToManyField(blank=True, to='page.benifit'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='educational_requirements',
            field=models.ManyToManyField(blank=True, to='page.educationalrequirement'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='experience_requirements',
            field=models.ManyToManyField(blank=True, to='page.experiencerequirement'),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_responsibilities',
            field=models.ManyToManyField(blank=True, to='page.responsibility'),
        ),
    ]
