from django.db import models

class ThemeManager(models.Manager):
    pass


class ThemeQuerySet(models.QuerySet):
    pass


class ChoiceManager(models.Manager):
    pass


class ChoiceQuerySet(models.QuerySet):
    pass


class MainCategoryManager(models.Manager):
    def get_queryset(self):
        query = super(MainCategoryManager, self).get_queryset().filter(
            parent__isnull=True
        )
        return query

class CategoryManager(models.Manager):
    def get_cat_with_children(self):
        t = []
        categories = self.filter(
            parent__isnull=True
        )
        return categories

        children = self.filter(
            children__gte=0
        )
        print("categories : ", categories)

        return categories | children
        # for cat in categories:
        #     print("----------------------------")
        #
        #     t.append(cat)
        #     print("category : ", cat)
        #     print("cat.children : ", cat.children)
        #     print("cat.children : ", cat.children.count())
        #     if cat.children.count() > 0:
        #         print("cat.children.all() : ", cat.children.all())
        #         # t.append(cat.children.all())
        #     # children_cat = categories.objects.filter(parent=category.id)
        #     # print("children_cat : ", children_cat)
        #     # t.append(children_cat)
        # return t
            
    def del_all_counter(self):
        for category in self.all():
            category.del_counter()
            category.theme.del_counter()

    def add_all_counter(self):
        for category in self.all():
            category.add_counter()
            category.theme.add_counter()


class CategoryQuerySet(models.QuerySet):
    pass
