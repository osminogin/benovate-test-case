# Generated by Django 2.2 on 2019-04-10 13:52

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_load_fixtures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='inn_number',
            field=models.CharField(max_length=12, unique=True, validators=[users.validators.INNValidator()]),
        ),
    ]
