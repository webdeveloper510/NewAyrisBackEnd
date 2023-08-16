from typing import Any

from django.db import models
from accounts.models import CustomUser


from .manager import (
CatPrefManager,
UserPreferenceManager
)

from category.models import (
Period,
People,
Thing,
Place,
Style,
Profession
)

from machine.models import (
MenuOrder,
MenuCategoryUser
)

from artworks.models import (
Medium,
Matter,
Color
)


class CatPref(MenuCategoryUser):
    objects = CatPrefManager()

    class Meta:
        proxy = True


class ArtWorkPref(models.Model):
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

    class Meta:
        db_table = "pref_art"

EXPT_OBJ = (
    'mediums',
    'matters',
    'colors'
)

class UserPreference(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="prefers",
        null=True,
    )

    peoples = models.ManyToManyField(
        People,
        blank=True
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
        blank=True
    )

    styles = models.ManyToManyField(
        Style,
        blank=True
    )

    professions = models.ManyToManyField(
        Profession,
        blank=True
    )

    art_works = models.OneToOneField(
        ArtWorkPref,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = UserPreferenceManager()

    class Meta:
        db_table = "pref_user"

    def __str__(self):
        return self.user.email if self.user else "No user"

    @property
    def categories(self):
        import sys
        serialized = False
        if sys._getframe(1).f_code.co_name == 'get_categories':
            serialized = True

        cats = CatPref.objects.filter(user=self.user_id)
        if serialized:
            return list(cats.values("order", "category__name__str"))
        return cats

    def sample_method(self):
        import sys
        param = None
        try:
            param = sys._getframe(1).f_code.co_name.split('_')[1]
        except:
            raise Exception("ERoor with sys._getframe")
        else:
            print("param", param)
            if param and isinstance(param, str):
                attr_obj, attr_name = None, param
                if attr_name in EXPT_OBJ:
                    attr_obj = getattr(self, "art_works")
                attr_obj = getattr(self, attr_name) if not attr_obj else getattr(attr_obj, attr_name)
                return list(attr_obj.values_list('name', flat=True))
            else:
                raise Exception("NO a STRING")

    @property
    def get_peoples(self):
        return self.sample_method()

    @property
    def get_places(self):
        return self.sample_method()

    @property
    def get_things(self):
        return self.sample_method()

    @property
    def get_periods(self):
        return self.sample_method()

    @property
    def get_styles(self):
        return self.sample_method()


    @property
    def get_profs(self):
        return self.sample_method()


    @property
    def get_mediums(self):
        return self.sample_method()


    @property
    def get_colors(self):
        return self.sample_method()


    @property
    def get_matters(self):
        return self.sample_method()



