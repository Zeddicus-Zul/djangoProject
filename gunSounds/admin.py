from django.contrib import admin
from .models import Gun, AudioClip
# Register models here

@admin.action(description="Test")
class AudioClipInline(admin.TabularInline):
    model = AudioClip
    extra = 5  # Shows 5 empty slots for new objects by default


class GunAdmin(admin.ModelAdmin):
    inlines = [AudioClipInline]
    list_display = ('name', 'ammo_type', 'size')  #  show these in list view
    search_fields = ('name', 'ammo_type')         #  add search box

admin.site.register(Gun, GunAdmin)
