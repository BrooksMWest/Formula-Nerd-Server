# Generated by Django 4.2.19 on 2025-03-09 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulanerdapi', '0004_alter_circuit_year_built'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circuit',
            name='nation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='formulanerdapi.nation'),
        ),
    ]
