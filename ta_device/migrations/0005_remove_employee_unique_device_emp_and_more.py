# Generated by Django 4.0.5 on 2024-05-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_device', '0004_alter_employee_emp_id_no'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='employee',
            name='unique_device_emp',
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.UniqueConstraint(fields=('device', 'device_id_no'), name='unique_device_emp'),
        ),
    ]
