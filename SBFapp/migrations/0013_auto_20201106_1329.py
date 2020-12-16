# Generated by Django 3.1.1 on 2020-11-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SBFapp', '0012_auto_20201106_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='days',
            field=models.ManyToManyField(to='SBFapp.Recurrence', verbose_name='Repeat'),
        ),
        migrations.AlterField(
            model_name='recurrence',
            name='choice',
            field=models.CharField(choices=[('Monday', 'mon'), ('Tuesday', 'tue'), ('Wednesday', 'wed'), ('Thursday', 'thu'), ('Friday', 'fri'), ('Saturday', 'sat'), ('Sunday', 'sun')], max_length=10, unique=True),
        ),
    ]
