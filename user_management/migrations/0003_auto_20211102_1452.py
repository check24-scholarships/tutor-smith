# Generated by Django 3.2.6 on 2021-11-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='show_address',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='show_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='settings',
            name='show_phone',
            field=models.BooleanField(default=False),
        ),
    ]