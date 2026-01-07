from django.contrib import admin
from .models import Gun, AudioClip, Score, MapMarker

class AudioClipInline(admin.TabularInline):
    model = AudioClip
    extra = 0

class GunAdmin(admin.ModelAdmin):
    inlines = [AudioClipInline]
    list_display = ('name', 'ammo_type', 'size')
    search_fields = ('name', 'ammo_type')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'high_score')
    search_fields = ('user__username',)
    readonly_fields = ('user',)

class MapMarkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'map_name', 'marker_type', 'latitude', 'longitude', 'created_at')
    list_filter = ('map_name', 'marker_type')
    search_fields = ('name',)

admin.site.register(Gun, GunAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(MapMarker, MapMarkerAdmin)
