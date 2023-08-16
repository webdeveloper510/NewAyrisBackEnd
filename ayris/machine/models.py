from django.db import models
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from ayris.custom.models import TimestampModel, MasterModel
from category.models import (
Category,
MainCategory
)

from .manager import (
MachineQuerySet,
MachineManager
)

from accounts.models import CustomUser


class Counter(TimestampModel):

    visitor_counter = MasterModel.set_basic_integer('Visitor Counter')
    past_counter = MasterModel.set_basic_integer('Leave Past Counter')
    future_counter = MasterModel.set_basic_integer('Onwards Future Counter')

    # def __str__(self):
    #     return f"visitor_counter: {self.visitor_counter} - " \
    #            f"past_counter : {self.past_counter} - " \
    #            f"future_counter: {self.future_counter}"

    def add_visitor_counter(self):
        self.visitor_counter += 1
        self.save()

    def add_past_counter(self):
        self.past_counter += 1
        self.save()

    def add_future_counter(self):
        self.future_counter += 1
        self.save()


class Machine(models.Model):

    name = models.CharField(
        _('Machine name'),
        max_length=40,
        unique=True
    )

    #TODO autocreate
    counter = models.OneToOneField(
        Counter,
        on_delete=models.CASCADE,
        null=True
    )
    manifesto = HTMLField(
        default=""
    )

    manual = HTMLField(
        default=""
    )

    objects = MachineManager().from_queryset(MachineQuerySet)()

    class Meta:
        db_table = "machine"

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.name == '':
            raise ValidationError('Empty error name')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        print("self.counter : ", self.counter)
        if not self.counter:
            self.counter = Counter.objects.create()
            print("self.counter CREate: ", self.counter)
        print("self.__dict__ : ", self.__dict__)
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.counter:
            self.counter.delete()
        return super().delete(using, keep_parents)


class New(TimestampModel):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="news",
        null=True
    )

    text = models.TextField(
        _('News'),
        max_length=500
    )

    def __str__(self):
        return self.text


def template_path():
    return os.path.join(settings.MEDIA_ROOT, 'template_root')


class Template(TimestampModel):
    name = MasterModel.set_basic_field(
        models.CharField,
        'template name',
        max_length=50
    )

    path = models.FilePathField(
        path=template_path,
        allow_files=False,
        allow_folders=True,
        recursive=True
    )

    def __str__(self):
        return self.name

    #for USERs
    def get_all_template(self):
        pass
    #
    # @property
    # def get_path(self):
    #     return self.path


class Config(models.Model):
    template = models.OneToOneField(
        Template,
        on_delete=models.CASCADE,
        default=1
    )

    machine = models.OneToOneField(
        Machine,
        on_delete=models.CASCADE,
        null=True,
        related_name="config"
    )

    # TODO SET ORDER FROM Category theme
    collumn_order = models.Empty()

    #TODO SET IF Category theme AND devise by 2
    limit_by_collumn = models.PositiveSmallIntegerField(
        default=0
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_page_count_range",
                check=models.Q(limit_by_collumn__range=(0, 50)),
            ),
        ]

    def __str__(self):
        return f"template : {self.template}"

    def auto_set_limit_by_collumn(self):
        theme_counts = Category.objects.count()
        if theme_counts > 1:
            self.limit_by_collumn = int(theme_counts / 2)
            print("NEW self.limit_by_collumn : ", self.limit_by_collumn)

    #TODO template check to set auto_set_limit_by_collumn
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.auto_set_limit_by_collumn()
        super().save(force_insert, force_update, using, update_fields)


class MenuOrder(models.Model):
    # order = models.AutoField(
    #     primary_key=True
    # )

    order = models.PositiveSmallIntegerField(
        # default=0,
        blank=True,
        auto_created=True,
        # unique=True,
        null=True
        # editable=False
    )

    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        abstract = True
        ordering = ["order"]

    def __str__(self):
        if self.category and hasattr(self.category, "name"):
            return f"Cat {self.order} : {self.category.name}"

    @classmethod
    def set_order(cls, class_name, user_id=None):
        # raise Exception(class_name)
        last_order, check = None, False

        if class_name == "MenuCategory":
            if MenuCategory.objects.exists():
                last_order = MenuCategory.objects.last().order
                check = True
        if class_name == "MenuCategoryUser":
            # raise Exception(MenuCategoryUser.objects.filter(user_id=user_id).count())
            cat_user = MenuCategoryUser.objects.filter(user_id=user_id)
            print("cat_user", cat_user)
            print("cat_user.count()", cat_user.count())
            if user_id and cat_user.count() > 0:
                last_order = cat_user.last().order
                print("cat_user.last()", cat_user.last())
                print("last_order", last_order)
                check = True
                print("check", check)

        # if check:
        #     order = last_order + 1
        # else:
        #     order = 0
        print("check", check)
        return last_order + 1 if check else 0

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.pk:
            class_name = self.__class__.__name__

            if self.__class__.__name__ == "MenuCategory":
                print("self.__dict__ : ", self.__dict__)
                print("self.category.parent : ", self.category.parent)
                if not self.category.parent:
                    self.order = MenuOrder.set_order(class_name)
                else:
                    raise Exception("Only main Category")
            # if self.__class__.__name__ == "MenuCategory":
            #     if MenuCategory.objects.exists():
            #         last_order = MenuCategory.objects.last().order
            #         check = True
            # if self.__class__.__name__ == "MenuCategoryUser":
            #     if MenuCategoryUser.objects.exists():
            #         last_order = MenuCategoryUser.objects.last().order
            #         check = True

            # if self.__class__.__name__ == "UserCatPref":
            #     from prefered.models import UserCatPref
            #     if UserCatPref.objects.exists():
                    # order = UserCatPref.objects.
                    # last_order = UserCatPref.objects.last().order
                    # check = True

            # if check:
            #     self.order = last_order + 1
            # else:
            #     self.order = 0

        super().save(force_insert, force_update, using, update_fields)


class MenuCategory(MenuOrder):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="menu",
        null=True
    )

    # TODO set save with only parent == None

    class Meta:
        db_table = "machine_menu"


class MenuCategoryUser(MenuOrder):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="menu"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        null=True
    )

    # TODO ADD constraint max 9 (OR other limit)
    class Meta:
        db_table = "machine_menu_user"
        unique_together = ('order', 'user')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'],
                name='unic_user_cat'
            )
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # raise Exception(MenuCategoryUser.objects.last())
        if not self.pk:
            class_name = self.__class__.__name__
            print("class_name", class_name)
            self.order = MenuOrder.set_order(class_name, self.user_id)
            print("self.order", self.order)
            print("-------------------------")
            print("-------------------------")

        super().save(force_insert, force_update, using, update_fields)



class Circle(models.Model):
    circle_name = models.CharField(
        _('Name of Circle'),
        max_length=40,
        unique=True,
        null=True
    )

    circle_type = models.CharField(
        _('Type of Circle'),
        max_length=40,
        unique=True,
        null=True
    )

    circle_number = models.PositiveSmallIntegerField(
        blank=True,
        auto_created=True,
        unique=True,
        null=True
    )

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        null=True,
        related_name="circles"
    )

    def __str__(self):
        return f"{self.circle_number}: {self.circle_name}  - {self.circle_type}"

    # TODO Custom  circle number if update
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.pk:
            if not Circle.objects.exists():
                self.circle_number = 1
            else:
                # raise Exception(self.circle_number)
                self.circle_number = Circle.objects.last().circle_number + 1
        # else:
        #     raise Exception(Circle.objects.filter(circle_number=self.circle_number + 1))
        # raise Exception(self.circle_number)

        super().save(force_insert, force_update, using, update_fields)


