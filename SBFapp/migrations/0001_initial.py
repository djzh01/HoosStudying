# Generated by Django 3.1.1 on 2020-10-22 19:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(blank=True, default='Enter Major', max_length=40)),
                ('year', models.CharField(blank=True, choices=[('First Year', '1st'), ('Second Year', '2nd'), ('Third Year', '3rd'), ('Fourth Year', '4th')], default='First', max_length=20)),
                ('max_group_size', models.CharField(blank=True, choices=[('Max Two People', '2'), ('Max Three People', '3'), ('Max Four People', '4'), ('Max Five or More People', '5 >')], default='Two', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=60)),
                ('event_description', models.TextField()),
                ('event_start_time', models.TimeField(default=datetime.datetime(2020, 10, 22, 15, 19, 27, 734272), verbose_name='Start Time')),
                ('event_end_time', models.TimeField(default=datetime.datetime(2020, 10, 22, 16, 19, 27, 734272), verbose_name='End Time')),
                ('event_date', models.DateField(default=datetime.date(2020, 10, 22), verbose_name='Date')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
