# Generated by Django 4.2.4 on 2023-08-11 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workingtime', '0003_alter_timesheet_datetime_complete_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktime',
            name='time_worked_per_day',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
