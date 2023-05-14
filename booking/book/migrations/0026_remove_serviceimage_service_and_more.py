# Generated by Django 4.2 on 2023-05-06 18:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0025_alter_availabletimeslot_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceimage',
            name='service',
        ),
        migrations.AddField(
            model_name='serviceimage',
            name='service_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.servicetype'),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 5, 18, 4, 21, 104492, tzinfo=datetime.timezone.utc)),
        ),
    ]