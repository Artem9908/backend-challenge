from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EventOutbox",
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
                ("event_type", models.CharField(max_length=255)),
                (
                    "event_date_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("environment", models.CharField(max_length=255)),
                ("event_context", models.JSONField()),
                ("metadata_version", models.IntegerField(default=1)),
                ("processed", models.BooleanField(default=False)),
                ("processed_at", models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
