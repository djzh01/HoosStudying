# Generated by Django 3.1.2 on 2020-11-19 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SBFapp', '0020_profile_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.TextField()),
                ('group_descr', models.TextField()),
                ('max_members', models.CharField(blank=True, choices=[('Max Two People', '2'), ('Max Three People', '3'), ('Max Four People', '4'), ('Max Five or More People', '5 >')], default='Two', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
