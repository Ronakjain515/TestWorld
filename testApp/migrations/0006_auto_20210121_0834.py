# Generated by Django 3.1.5 on 2021-01-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0005_test_user_questions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='timer',
            new_name='timer_minutes',
        ),
        migrations.AddField(
            model_name='test',
            name='timer_seconds',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
