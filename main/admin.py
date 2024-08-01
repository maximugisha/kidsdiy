from django.contrib import admin
from main.models import account_info, Room, Room_member, MeetingWhiteboard, Room_message, Attendence_report, meeting_schedule, Role, Interest,  Organization

admin.site.register(account_info)
admin.site.register(Room_member)
admin.site.register(Room)
admin.site.register(meeting_schedule)
admin.site.register(Attendence_report)
admin.site.register(Room_message)
admin.site.register(MeetingWhiteboard)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile_pic']
