# Generated by Django 4.2.19 on 2025-03-08 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulanerdapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='age',
            field=models.IntegerField(null=True),
        ),
    ]
