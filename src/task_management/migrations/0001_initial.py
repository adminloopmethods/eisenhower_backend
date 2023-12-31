# Generated by Django 4.2.2 on 2023-09-01 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrix', '0001_initial'),
        ('configuration', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=100)),
                ('customer_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('estimate', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('reminder', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.departments')),
                ('matrix_type_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrix.matrixtaskmapping')),
                ('members', models.ManyToManyField(blank=True, null=True, to='user.customusers')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.taskstatusmaster')),
                ('task_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_owner_user', to='user.customusers')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configuration.topics')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Tasks',
                'verbose_name_plural': 'Tasks',
                'db_table': 'tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskComments',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('members', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customusers')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.tasks')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Task Comments',
                'verbose_name_plural': 'Task Comments',
                'db_table': 'task_comments',
            },
        ),
    ]
