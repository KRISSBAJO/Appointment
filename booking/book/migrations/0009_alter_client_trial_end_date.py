# Generated by Django 4.2 on 2023-04-29 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_alter_client_trial_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 29, 20, 14, 47, 29082, tzinfo=datetime.timezone.utc)),
        ),
    ]
