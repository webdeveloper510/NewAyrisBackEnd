from django.contrib import admin

from .models import (
    Category,
    Thing,
    People,
    Place,
    Period,
    Profession,
    Style
)


class CommonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'counter', )


class CategoryAdmin(CommonAdmin):
    list_display = CommonAdmin.list_display + ('theme', )


class ThemeAdmin(CommonAdmin):
    pass

admin.site.register(Category)
admin.site.register(Thing)
admin.site.register(People)
admin.site.register(Place)
admin.site.register(Period)
admin.site.register(Profession)
admin.site.register(Style)
