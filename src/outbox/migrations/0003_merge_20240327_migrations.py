from django.db import migrations


class Migration(migrations.Migration):
    """
    Merge migration for handling multiple 0002 migrations
    """
    
    dependencies = [
        ('outbox', '0002_auto_20240327'),
        ('outbox', '0002_alter_eventoutbox_event_date_time_and_more'),
    ]

    operations = [] 