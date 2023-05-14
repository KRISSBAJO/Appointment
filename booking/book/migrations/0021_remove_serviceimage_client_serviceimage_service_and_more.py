# Generated by Django 4.2 on 2023-05-03 20:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0020_service_describe_service_alter_client_trial_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceimage',
            name='client',
        ),
        migrations.AddField(
            model_name='serviceimage',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_images', to='book.service'),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 2, 20, 4, 6, 613803, tzinfo=datetime.timezone.utc)),
        ),
    ]
