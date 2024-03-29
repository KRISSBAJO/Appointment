# Generated by Django 4.2 on 2023-05-06 21:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0026_remove_serviceimage_service_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 5, 21, 46, 25, 234460, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='service',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book.client'),
        ),
    ]
