from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('outbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoutbox',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='eventoutbox',
            table='outbox_eventoutbox',
        ),
    ]  