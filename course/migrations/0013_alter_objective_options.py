# Generated by Django 3.2.13 on 2024-01-12 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_objective'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objective',
            options={'ordering': ['order']},
        ),
    ]
