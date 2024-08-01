# Generated by Django 3.2.3 on 2022-12-26 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.TextField(unique=True)),
                ('chats', models.BooleanField(default=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('passcode', models.TextField(blank=True, null=True)),
                ('room_type', models.CharField(default='meeting', max_length=30)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('time_limit', models.IntegerField(default=2400)),
                ('room_id', models.TextField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room_member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=30)),
                ('time_joined', models.DateTimeField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='whiteboard_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.TextField()),
                ('file', models.FileField(upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='Room_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='media')),
                ('file_type', models.CharField(blank=True, max_length=30, null=True)),
                ('file_name', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
                ('room_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.room_member')),
            ],
        ),
        migrations.CreateModel(
            name='RecordedFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileUrl', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingWhiteboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_token', models.TextField(blank=True, null=True)),
                ('room_uuid', models.TextField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
        ),
        migrations.CreateModel(
            name='meeting_schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_title', models.TextField()),
                ('meeting_time', models.DateTimeField()),
                ('uer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendence_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_joined', models.DateTimeField(blank=True, null=True)),
                ('time_left', models.DateTimeField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='account_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datejoined', models.DateField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, default='no_profile_Pic.jpeg', upload_to='profile_pics')),
                ('description', models.TextField(blank=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('user_token', models.TextField(unique=True)),
                ('email_token', models.CharField(blank=True, max_length=200, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('username', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]