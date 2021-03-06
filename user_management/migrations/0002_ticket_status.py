# Generated by Django 3.2.5 on 2021-11-02 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(
                choices=[
                    (1, 'Rejected'),
                    (2, 'Review Pending'),
                    (3, 'Reviewing'),
                    (4, 'Finished'),
                ],
                default=2,
            ),
        ),
    ]
