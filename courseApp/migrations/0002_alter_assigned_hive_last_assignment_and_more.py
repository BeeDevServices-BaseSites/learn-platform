# Generated by Django 4.2.7 on 2024-03-06 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigned_hive',
            name='last_assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theAssignment', to='courseApp.reading'),
        ),
        migrations.AlterField(
            model_name='assigned_hive',
            name='last_reading',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theReading', to='courseApp.reading'),
        ),
    ]
