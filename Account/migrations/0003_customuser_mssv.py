# Generated by Django 5.2 on 2025-04-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_customuser_role_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mssv',
            field=models.CharField(default='', max_length=10),
        ),
    ]
