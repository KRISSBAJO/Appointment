# Generated by Django 4.2 on 2023-05-02 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_remove_newslettersubscriber_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 1, 18, 22, 13, 526321, tzinfo=datetime.timezone.utc)),
        ),
    ]