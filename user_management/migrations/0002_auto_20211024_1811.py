# Generated by Django 3.2.7 on 2021-10-24 16:11

from django.db import migrations, models
import stdimage.models
import user_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='certificate',
            field=models.BinaryField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=stdimage.models.JPEGField(
                blank=True,
                default=None,
                null=True,
                upload_to=user_management.models.image_pic_path,
            ),
        ),
    ]