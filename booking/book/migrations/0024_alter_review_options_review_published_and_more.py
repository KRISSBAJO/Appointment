# Generated by Django 4.2 on 2023-05-05 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0023_remove_usersubscription_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AddField(
            model_name='review',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 4, 16, 8, 37, 357801, tzinfo=datetime.timezone.utc)),
        ),
    ]
