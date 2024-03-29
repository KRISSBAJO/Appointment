# Generated by Django 4.2 on 2023-05-06 15:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0024_alter_review_options_review_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabletimeslot',
            name='client',
            field=models.ForeignKey(help_text='Select the client offering this time slot', on_delete=django.db.models.deletion.CASCADE, to='book.client'),
        ),
        migrations.AlterField(
            model_name='availabletimeslot',
            name='date',
            field=models.DateField(help_text='Enter the date for the time slot'),
        ),
        migrations.AlterField(
            model_name='availabletimeslot',
            name='is_booked',
            field=models.BooleanField(default=False, help_text='Indicates if the time slot has been booked'),
        ),
        migrations.AlterField(
            model_name='availabletimeslot',
            name='service',
            field=models.ForeignKey(help_text='Select your service', on_delete=django.db.models.deletion.CASCADE, to='book.service'),
        ),
        migrations.AlterField(
            model_name='availabletimeslot',
            name='time',
            field=models.TimeField(help_text='Enter the time for the time slot'),
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 5, 15, 43, 37, 581191, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.DurationField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.service')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='service_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='book.servicetype'),
        ),
    ]
