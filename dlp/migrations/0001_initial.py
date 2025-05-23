# Generated by Django 5.2 on 2025-04-08 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('regex', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_ts', models.CharField(max_length=100, unique=True)),
                ('user', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pattern', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dlp.pattern')),
            ],
        ),
    ]
