# Generated by Django 4.2 on 2023-05-14 04:33

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0028_client_city_client_country_client_state_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='price',
        ),
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 13, 4, 33, 29, 403507, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='SubscriptionPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.subscription')),
            ],
        ),
    ]
