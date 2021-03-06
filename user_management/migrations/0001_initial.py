# Generated by Django 3.2.5 on 2021-10-31 14:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import stdimage.models
import user_management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
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
                    'subject',
                    models.IntegerField(
                        choices=[
                            (0, 'Deutsch'),
                            (1, 'Mathe'),
                            (2, 'Englisch'),
                            (3, 'Chemie'),
                            (4, 'Informatik'),
                        ]
                    ),
                ),
                ('description', models.TextField()),
                (
                    'level_class',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(12),
                            django.core.validators.MinValueValidator(5),
                        ]
                    ),
                ),
                (
                    'difficulty',
                    models.IntegerField(
                        choices=[(0, 'Beginner'), (1, 'Medium'), (2, 'Hard')]
                    ),
                ),
                (
                    'cost_budget',
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ('searching', models.BooleanField()),
                ('created_on', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
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
                    'email',
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        verbose_name='email address',
                    ),
                ),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=265)),
                (
                    'gender',
                    models.IntegerField(
                        choices=[
                            (9, 'Not Stated'),
                            (1, 'M??nnlich'),
                            (2, 'Weiblich'),
                            (3, 'Another Term'),
                        ]
                    ),
                ),
                (
                    'address',
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    'phone',
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        null=True,
                        region=None,
                        unique=True,
                    ),
                ),
                (
                    'user_class',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(12),
                            django.core.validators.MinValueValidator(5),
                        ]
                    ),
                ),
                ('description', models.TextField(default='')),
                ('birth_date', models.DateField()),
                ('created_on', models.DateTimeField()),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                (
                    'certificate',
                    models.BinaryField(blank=True, default=None, null=True),
                ),
                (
                    'profile_pic',
                    stdimage.models.JPEGField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to=user_management.models.image_pic_path,
                    ),
                ),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
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
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                (
                    'ticket_type',
                    models.IntegerField(
                        choices=[(1, 'Report'), (2, 'Bug'), (3, 'Request')]
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ticket_author',
                        to='user_management.user',
                    ),
                ),
                (
                    'for_user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ticket_for_user',
                        to='user_management.user',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
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
                ('show_email', models.BooleanField()),
                ('show_address', models.BooleanField()),
                ('show_phone', models.BooleanField()),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='user_management.user',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Review',
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
                ('title', models.CharField(max_length=24)),
                ('text', models.TextField()),
                (
                    'stars',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                ('created_on', models.DateTimeField()),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='Author',
                        to='user_management.user',
                    ),
                ),
                (
                    'for_user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='for_user',
                        to='user_management.user',
                    ),
                ),
            ],
        ),
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
        migrations.AddField(
            model_name='info',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='user_management.user',
            ),
        ),
        migrations.CreateModel(
            name='UserAuth',
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
                    'password',
                    models.CharField(max_length=128, verbose_name='password'),
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='first name'
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='last name'
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        verbose_name='email address',
                    ),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
