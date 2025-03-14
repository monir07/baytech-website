# Generated by Django 4.0.5 on 2025-03-08 10:33

import base.helpers.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page', '0002_project_proejct_category_alter_project_proejct_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='publish_date',
        ),
        migrations.CreateModel(
            name='NewsInsight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_line', models.CharField(max_length=150)),
                ('publish_date', models.DateField()),
                ('body', models.TextField()),
                ('cover_photo', models.ImageField(help_text='File size should be less than 3mb(.doc/.pdf)', upload_to='news/', validators=[base.helpers.validators.file_size_validator])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
