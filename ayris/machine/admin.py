from django.contrib import admin
from .models import (
Machine,
New,
Counter,
Config,
Template,
MenuCategory,
MenuCategoryUser,
Circle
)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('category', 'order', )


admin.site.register(Template)
admin.site.register(MenuCategory, MenuAdmin)
admin.site.register(MenuCategoryUser, MenuAdmin)
admin.site.register(Config)
admin.site.register(Machine)
admin.site.register(Circle)
admin.site.register(New)
admin.site.register(Counter)
