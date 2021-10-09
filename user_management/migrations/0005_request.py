# Generated by Django 3.2.5 on 2021-10-03 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_auto_20211002_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='request_author',
                        to='user_management.user',
                    ),
                ),
                (
                    'for_user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='request_info_author',
                        to='user_management.user',
                    ),
                ),
                (
                    'info',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='info',
                        to='user_management.info',
                    ),
                ),
            ],
        ),
    ]
