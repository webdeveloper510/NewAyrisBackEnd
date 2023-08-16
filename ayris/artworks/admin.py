from django.contrib import admin

from .models import (
    Medium,
    Matter,
    Color,
    ArtWork
)


class CommonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'counter', )


admin.site.register(Medium)
admin.site.register(Matter)
admin.site.register(Color)
admin.site.register(ArtWork)


