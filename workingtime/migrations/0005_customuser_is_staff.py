# Generated by Django 4.2.4 on 2023-08-02 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workingtime', '0004_alter_employee_engaged_alter_employer_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]