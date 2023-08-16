from django.contrib import admin

from .models import (
Post,
PostType,
ComplainMessageCat,
ComplainMessage
)

class ComplainMessageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.sender = request.user
        super().save_model(request, obj, form, change)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'slug',
        # 'choice',
        'post_type'
    )

    # def delete_queryset(self, request, queryset):
    #     for q in queryset:
    #         q.category.del_all_counter()
    #     super().delete_queryset(request, queryset)

    def save_related(self, request, form, formsets, change):

        super(PostAdmin, self).save_related(request, form, formsets, change)
        # print("form.instance.category : ", form.instance.category)
        # print("form.instance.category : ", form.instance.category.all())
        # print("form.instance.choice : ", form.instance.choice)
        # #ADD COUNTER
        # if not change:
        #     form.instance.category.add_all_counter()

    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related('tags')
    #
    # def tag_list(self, obj):
    #     return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
admin.site.register(PostType)
admin.site.register(ComplainMessageCat)
admin.site.register(ComplainMessage, ComplainMessageAdmin)
