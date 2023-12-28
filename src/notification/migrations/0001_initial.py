# Generated by Django 4.2.2 on 2023-09-01 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationConfiguration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notification_main_type', models.CharField(max_length=100)),
                ('notification_type', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('notification_for', models.CharField(choices=[('member', 'member'), ('customer', 'customer'), ('manager', 'manager'), ('admin', 'Admin'), ('bcr_user', 'BCR')], max_length=50)),
                ('sample_content', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': ' Notification Configuration',
                'verbose_name_plural': ' Notification Configuration',
                'db_table': 'notification_configuration',
            },
        ),
        migrations.CreateModel(
            name='NotificationRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notification_category', models.CharField(choices=[('PUSH', 'PUSH'), ('SMS', 'SMS'), ('EMAIL', 'EMAIL')], max_length=20)),
                ('notification_to', models.CharField(choices=[('member', 'member'), ('customer', 'customer'), ('manager', 'manager'), ('admin', 'Admin'), ('bcr_user', 'BCR')], max_length=50)),
                ('reason_for_failed', models.TextField(blank=True, null=True, verbose_name='Reason For Non Delivery')),
                ('message_body', models.TextField(verbose_name='Notification Content')),
                ('is_read', models.BooleanField(default=False)),
                ('notify_at', models.DateTimeField(auto_now_add=True, verbose_name='Notification Date & Time')),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.notificationconfiguration')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customusers')),
            ],
            options={
                'verbose_name': 'Notification History',
                'verbose_name_plural': 'Notification History',
                'db_table': 'notification_record',
            },
        ),
        migrations.CreateModel(
            name='NotificationFirebaseToken',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('device_token', models.TextField(verbose_name='Fire base Token')),
                ('device_type', models.CharField(choices=[('android', 'Mobile/Android'), ('ios', 'Mobile/iOS'), ('web', 'Web')], max_length=30, verbose_name='Device Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customusers')),
            ],
            options={
                'verbose_name': 'Notification Firebase',
                'verbose_name_plural': 'Notification Firebase',
            },
        ),
    ]
