# Generated by Django 4.1.5 on 2023-02-01 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TAE', '0002_mastertae'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mastertae',
            old_name='Reason',
            new_name='Revenue_Reason',
        ),
        migrations.RemoveField(
            model_name='mastertae',
            name='Revenue',
        ),
    ]