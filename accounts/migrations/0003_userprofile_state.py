# Generated by Django 4.2.5 on 2023-10-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="state",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
