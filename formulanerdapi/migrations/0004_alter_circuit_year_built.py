# Generated by Django 4.2.19 on 2025-03-09 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulanerdapi', '0003_alter_constructor_is_engine_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circuit',
            name='year_built',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
