from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ayris.custom.models import TimestampModel
from .manager import (
CategoryManager,
CategoryQuerySet,
MainCategoryManager
)


class Generic(models.Model):

    name = models.CharField(
        max_length=30,
    )

    #TODO add unic  slug param with parent
    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True,
    )

    counter = models.PositiveIntegerField(
        default=0
    )

    is_allow = models.BooleanField(
        default=False
    )


    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class GenericObject(Generic):
    period = models.CharField(
        max_length=30,
        blank=True

    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)


class People(GenericObject):
    user_name = models.CharField(
        max_length=30,
        blank=True

    )


class Thing(GenericObject):
    def get_parent(self):
        return Category.objects.filter(things=self)

    def __str__(self):
        # k = [l.__str__() + ' -> ' + self.name for l in self.get_parent()]
        # return str(k)
        return self.name


class Place(GenericObject):
    def get_parent(self):
        return Category.objects.filter(places=self)

    def __str__(self):
        return self.name


class Period(GenericObject):
    pass


class Profession(Generic):
    pass


class Style(Generic):
    pass


class GenericCat(Generic):
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    description = models.TextField(
        max_length=200,
        blank=True
    )

    class Meta:
        abstract = True


    def get_slug(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        # print("full_path 1 : ", full_path)

        return full_path[::-1]

    def __str__(self):
        full_path = self.get_slug()
        return ' -> '.join(full_path)

    #TODO ADD MAIN_CAT SLUG

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        full_path = self.get_slug()
        if self.parent:
            full_path = ' '.join(full_path)
        self.slug = slugify(full_path)
        # print("self.slug : ", self.slug)
        # print("----------------------")
        super().save(force_insert, force_update, using, update_fields)


class Category(GenericCat):

    peoples = models.ManyToManyField(
        People,
        blank=True,
    )

    things = models.ManyToManyField(
        Thing,
        blank=True
    )

    places = models.ManyToManyField(
        Place,
        blank=True
    )

    periods = models.ManyToManyField(
        Period,
        blank=True,
    )

    objects = CategoryManager()

    class Meta:
        db_table = "category"
    #     # enforcing that there can not be two categories under a parent with same slug
        unique_together = ('name', 'slug', 'parent')
    #     # TODO Add constraint not cat.parent=null whith a parent=null
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["parent", "name"],
    #             name="unic_cat_parent_and_child"
    #         ),
    #     ]


class MainCategory(Category):
    objects = MainCategoryManager()

    class Meta:
        proxy = True

