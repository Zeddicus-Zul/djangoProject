from django.contrib import admin
from .models import Gun, AudioClip

class AudioClipInline(admin.TabularInline):
    model = AudioClip
    extra = 5 # number of extra forms to display
    max_num = 5  # maximum number of audio clips per gun


class GunAdmin(admin.ModelAdmin):
    inlines = [AudioClipInline]
    list_display = ('name', 'ammo_type', 'size')  #  show these in list view
    search_fields = ('name', 'ammo_type')         #  add search box

admin.site.register(Gun, GunAdmin)
