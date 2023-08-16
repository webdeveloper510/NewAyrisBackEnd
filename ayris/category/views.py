from rest_framework import viewsets

from .serializers import (
CategorySerializer,
MenuCategorySerializer
)

from .models import (
Category,
)


class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        parent__isnull=True
    )
    serializer_class = MenuCategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#
#     def get_queryset(self):
#         print(self.kwargs)
#         print("type(self.kwargs.get('pk')) : ", type(self.kwargs.get('pk')))
#         if "pk" in self.kwargs:
#             if isinstance(self.kwargs.get("pk"), str):
#                 cat_slug = self.kwargs.get("pk")
#                 print("cat_slug : ", cat_slug)
#                 # TODO avoid pk OR add CHECK
#
#                 # print("machine_id", machine_id)
#                 # print("machine_id", type(machine_id))
#                 # print("machine :", machine_model.Machine.objects.filter(pk=machine_id))
#                 cat = Category.objects.filter(slug=cat_slug)
#                 print("cat : ", cat)
#                 return Category.objects.all()
#                 return cat if cat else None
#             else:
#                 raise Exception("Is not a string")
#
#         return Category.objects.all()
#         # q1 = Category.objects.filter(name=)
#         # q2 = Category.objects.filter(id__lte=9)
# #         """
# #         This view should return a list of all the purchases
# #         for the currently authenticated user.
# #         """
#         return Category.objects.get_cat_with_children()
# #
#
# class CatAndChildrenViewSet(viewsets.ModelViewSet):
#     # queryset = Category.objects.all()
#     queryset = Category.objects.filter(
#         parent__isnull=True
#     )
#     serializer_class = CatAndChildrenSerializer
#
#     # def filter_queryset(self, queryset):
#     #     print("queryset : ", queryset)
#     #     queryset = queryset.filter(children__isnull=False)
#     #     return super().filter_queryset(queryset)
#
# class ThemeChoiceViewSet(viewsets.ModelViewSet):
#     queryset = ThemeChoice.objects.all()
#     serializer_class = ThemeChoiceSerializer
