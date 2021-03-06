# Generated by Django 2.2.13 on 2020-07-19 19:05

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
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.CharField(max_length=30, verbose_name='Environment')),
                ('level', models.CharField(choices=[('error', 'ERROR'), ('info', 'INFO'), ('debug', 'DEBUG'), ('warning', 'WARNING'), ('critical', 'CRITICAL')], max_length=10, verbose_name='Level')),
                ('message', models.CharField(max_length=200, verbose_name='Message')),
                ('origin', models.GenericIPAddressField(protocol='IPv4', verbose_name='Origin')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('is_archived', models.BooleanField(verbose_name='Is archived')),
                ('events', models.IntegerField(verbose_name='Events')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
