# Generated by Django 4.2.11 on 2024-05-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0024_remove_userdailystatistic_total"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDailyAddition",
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
                ("date", models.DateField()),
                ("addition", models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name="UserDailyStatistic",
        ),
    ]
