# Generated by Django 5.1.1 on 2024-09-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enigma", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answers",
            name="equipe_id",
        ),
        migrations.AddField(
            model_name="answers",
            name="equipe",
            field=models.CharField(default="", max_length=64),
        ),
    ]
