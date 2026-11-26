from django.contrib import admin
from .models import Entry
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_mark', 'form_number', 'subject', 'account', 'friends', 'frieds')

    def friends(self, obj):
        try:
            url = reverse('login')
        except Exception:
            url = '/accounts/login/'
        return format_html('<a href="{}">ENTRIES</a>', url)
    friends.short_description = 'ENTRIES'

    def frieds(self, obj):
        try:
            url = reverse('admins')
        except Exception:
            # 'admins' URL does not exist - fall back to password change page
            url = '/admin/password_change/'
        return format_html('<a href="{}">CHANGE ADMIN PASSWORD</a>', url)
    frieds.short_description = 'CHANGE ADMIN PASSWORD'
