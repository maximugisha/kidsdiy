from django.db import models
from django.contrib.auth.models import User
from datetime import date

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["id"]  # Set your default ordering here


class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interest(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Organization(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.name

class account_info(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True, related_name='account')
    # datejoined = models.DateField(blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics', default='no_profile_Pic.jpeg')
    description = models.TextField(blank=True)
    # link = models.TextField(blank=True,null=True)
    # user_token = models.TextField(unique=True)
    # email_token = models.CharField(max_length=200, null=True, blank=True)
    # email_verified = models.BooleanField(default=False)
    # first_name = models.TextField(null=True, blank=True)
    # last_name = models.TextField(null=True, blank=True)
    # username = models.TextField(null=True, blank=True)
    biography = models.TextField(max_length=500, blank=True, null=True)
    interests = models.ManyToManyField(Interest, related_name='students', blank=True)
    roles = models.ForeignKey(Role, related_name='user_role', blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='user_organization',
                                     blank=True, null=True, on_delete=models.CASCADE
                                     )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)
    
    @property
    def bio(self):
        if self.biography:
            return self.biography[:150]
        else:
            return ""
        
        

class Room(models.Model):
    room_name = models.TextField(unique=True)
    chats = models.BooleanField(default=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    passcode = models.TextField(blank=True, null=True)
    room_type = models.CharField(max_length=30, default='meeting')
    start_date = models.DateTimeField(blank=True, null=True)
    time_limit = models.IntegerField(default=2400)
    room_id = models.TextField(unique=True, null=True)

class Room_member(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=30)
    time_joined = models.DateTimeField(blank=True, null=True)

class Room_message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_member = models.ForeignKey(Room_member, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='media')
    file_type = models.CharField(max_length=30, blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

class Attendence_report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(blank=True, null=True)
    time_left = models.DateTimeField(blank=True, null=True)

class meeting_schedule(models.Model):
    uer = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting_title = models.TextField()
    meeting_time = models.DateTimeField()

class MeetingWhiteboard(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_token = models.TextField(blank=True, null=True)
    room_uuid = models.TextField(blank=True, null=True)

class whiteboard_files(models.Model):
    room_name = models.TextField()
    file = models.FileField(upload_to='media')

class RecordedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fileUrl = models.TextField()


