# Generated by Django 5.0.6 on 2024-06-11 17:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chat_time", models.DateTimeField()),
                ("query", models.TextField()),
                ("answer", models.TextField()),
                ("sim1", models.FloatField()),
                ("sim2", models.FloatField()),
                ("sim3", models.FloatField()),
            ],
        ),
    ]
