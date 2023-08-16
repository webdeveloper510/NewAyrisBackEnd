from django.contrib import admin

from .models import (
Build,
ImageBuild,
Shield,
Banner,
ObjectName,
Album,
AlbumCategory
)


class BuildAdmin(admin.ModelAdmin):
    model = Build
    # fields = ('user', )
    list_display = (
        'user',
        'title',
        'artist_name',
        'image',
        'image_tag',
        'banner',
        'shield'
    )
    # list_display = ('user', 'title', 'artist_name', 'image', 'image_tag',)
    #
    # readonly_fields = ('image_tag',)

    """
    TO SET ObjectName is approuve
    """
    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     if obj.user and obj.user.is_superuser:
    #         print("obj.user : ", obj.user)
    #         print("obj : ", obj)
    #         print("form : ", form)
    #         print("change : ", change)
    #     super().save_model(request, obj, form, change)


admin.site.register(Build, BuildAdmin)
admin.site.register(ImageBuild)
admin.site.register(Shield)
admin.site.register(Banner)
admin.site.register(ObjectName)
admin.site.register(Album)
admin.site.register(AlbumCategory)
