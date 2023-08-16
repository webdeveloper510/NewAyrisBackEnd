from django.contrib import admin


from .models import (
ArtWorkPref,
UserPreference,
CatPref
)


class CatPrefAdmin(admin.ModelAdmin):
    list_display = ("category", "order")


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", )

    # TO DISPLAY A FILTER BY USER ON ATTR from model
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "categories":
    #         kwargs["queryset"] = CatPref.objects.filter(user=request.user)
    #     return super(UserPreferenceAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(CatPref, CatPrefAdmin)
admin.site.register(ArtWorkPref)
admin.site.register(UserPreference, UserPreferenceAdmin)
