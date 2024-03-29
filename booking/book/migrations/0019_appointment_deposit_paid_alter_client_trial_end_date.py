# Generated by Django 4.2 on 2023-05-03 16:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_service_deposit_amount_service_deposit_required_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='deposit_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 2, 16, 56, 58, 126729, tzinfo=datetime.timezone.utc)),
        ),
    ]
