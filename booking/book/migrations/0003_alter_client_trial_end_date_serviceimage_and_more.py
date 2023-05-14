# Generated by Django 4.1.7 on 2023-04-26 23:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_client_trial_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='trial_end_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 26, 23, 45, 14, 401463, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_images/')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_images', to='book.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profile_images/')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book.client')),
            ],
        ),
    ]