from django.contrib import admin
from .models import Gun, AudioClip
# Register your models here.

class AudioClipInline(admin.TabularInline):
    model = AudioClip
    extra = 10  # Shows 10 empty slots for new clips by default

class GunAdmin(admin.ModelAdmin):
    inlines = [AudioClipInline]
    list_display = ('name', 'ammo_type', 'size')  # optional: show these in list view
    search_fields = ('name', 'ammo_type')         # optional: add search box

admin.site.register(Gun, GunAdmin)
