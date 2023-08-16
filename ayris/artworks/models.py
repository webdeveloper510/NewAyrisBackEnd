from django.db import models
from category.models import (
GenericObject,
GenericCat
)

from django.utils.text import slugify

class Medium(GenericObject):
    period = models.Empty()



class Matter(GenericObject):
    period = models.Empty()


class Color(GenericObject):
    period = models.Empty()


#
# class ObjectName(GenericObject):
#     parent = models.ForeignKey(
#         'self',
#         blank=True,
#         null=True,
#         related_name='children',
#         on_delete=models.CASCADE
#     )
#
#     is_approuve = models.BooleanField(
#         default=False
#     )
#
#     class Meta:
#         db_table = "build_obj_name"
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["parent", "name"],
#                 name="unic_parent_and_child"
#             ),
#         ]
#
#     def get_slug(self):
#         full_path = [self.name]
#         k = self.parent
#         while k is not None:
#             full_path.append(k.name)
#             k = k.parent
#         return full_path[::-1]
#
#     def __str__(self):
#         full_path = self.get_slug()
#         return ' -> '.join(full_path)
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         full_path = self.get_slug()
#         self.slug = slugify(full_path)
#         super().save(force_insert, force_update, using, update_fields)

class ArtWork(GenericObject):
    mediums = models.ManyToManyField(
        Medium,
        blank=True
    )

    matters = models.ManyToManyField(
        Matter,
        blank=True
    )

    colors = models.ManyToManyField(
        Color,
        blank=True
    )
