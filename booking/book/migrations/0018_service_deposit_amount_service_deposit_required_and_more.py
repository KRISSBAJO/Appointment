# Generated by Django 4.2 on 2023-05-03 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_client_disabled_alter_client_trial_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='deposit_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='service',
            name='deposit_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 2, 16, 44, 9, 839907, tzinfo=datetime.timezone.utc)),
        ),
    ]
