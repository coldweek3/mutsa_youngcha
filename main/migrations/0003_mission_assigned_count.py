# Generated by Django 5.0.6 on 2024-05-18 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='assigned_count',
            field=models.IntegerField(default=0),
        ),
    ]
