from django.contrib import admin
from .models import Gun, AudioClip, Score

class AudioClipInline(admin.TabularInline):
    model = AudioClip

class GunAdmin(admin.ModelAdmin):
    inlines = [AudioClipInline]
    list_display = ('name', 'ammo_type', 'size')
    search_fields = ('name', 'ammo_type')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'high_score')
    search_fields = ('user__username',)
    readonly_fields = ('user',)

admin.site.register(Gun, GunAdmin)
admin.site.register(Score, ScoreAdmin)
