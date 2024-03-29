# Generated by Django 4.2 on 2023-04-30 00:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_alter_client_trial_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 30, 0, 26, 36, 679880, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='AvailableTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('is_booked', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.service')),
            ],
        ),
    ]
