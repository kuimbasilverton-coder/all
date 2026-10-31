from django.contrib import admin



from.models import Entry
from django.urls import reverse
from django.utils.html import format_html


    
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_mark', 'form_number', 'subject', 'account', 'friends', 'frieds')
    def friends(self, obj):
        url = reverse('login')
        return format_html('<a href="{}">ENTRIES</a>', url)

    friends.short_description = 'ENTRIES'
        
    def frieds(self, obj):
        url = reverse('admins')
        return format_html('<a href="{}">CHANGE ADMIN PASSWORD</a>', url)

    frieds.short_description = 'CHANGE ADMIN PASSWORD'    
    
    


    

          


    





    

    

    


