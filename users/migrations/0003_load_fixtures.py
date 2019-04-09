from django.db import migrations
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    call_command('loaddata', 'initial_data', app_label='users')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_balance'),
    ]

    operations = [
        migrations.RunPython(load_fixtures)
    ]
