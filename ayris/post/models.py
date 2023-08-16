from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField


from ayris.custom.models import (
TimestampModel,
MasterModel
)
from .manager import (
PostManager,
PostQuerySet
)
from category.models import (
Category,
# TopicObject,
Thing,
Place,
Period,
People
)

from artworks.models import ArtWork

from buildx.models import (
Image
)

class ImagePost(Image):
    class Meta:
        db_table = "post_image"


class ComplainMessageCat(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name


class ComplainMessage(TimestampModel):

    sender = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        ComplainMessageCat,
        on_delete=models.CASCADE,
    )

    comment = models.TextField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return "complain :" + self.category.__str__() + " - from : " + self.sender.email


class PostType(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )

    class Meta:
        db_table = "post_type"

    def __str__(self):
        return self.name.lower()


class Post(TimestampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=120)

    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True
    )

    post_type = models.ForeignKey(
        PostType,
        null=True,
        on_delete=models.CASCADE
    )

    art_work = models.OneToOneField(
        ArtWork,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    images = models.ManyToManyField(
        ImagePost,
        blank=True
    )

    category = models.ManyToManyField(
        Category,
        related_name="posts"
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

    content = HTMLField(
        default=""
    )

    is_approuved = models.BooleanField(
        default=False
    )

    like_counter = models.PositiveSmallIntegerField(
        default=0
    )

    dislike_counter = models.PositiveSmallIntegerField(
        default=0
    )

    complain_message = models.ManyToManyField(
        ComplainMessage,
        blank=True
    )

    # content = HTMLField('Content')
    # draft = models.BooleanField(default=False)
    # publish = models.DateField(auto_now=False, auto_now_add=False, )

    objects = PostManager().from_queryset(PostQuerySet)()


    class Meta:
        db_table = "post"
        # TODO ADD constraints to allow only attributes from MainCategory <= self.category
        # constraints = [
        #     models.CheckConstraint(
        #         check=models.Q(attribute__in=category.attributes.all()),
        #         name="%(app_label)s_%(class)s_gender_valid"
        #     )
        # ]

    def __str__(self):
        return self.title



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)

        self.clean_fields()
        print("self.__dict__ : ", self.__dict__)
        print("self.user.is_superuser : ", self.user.is_superuser)
        if self.user.is_superuser:
            self.is_approuved = True

        super().save(force_insert, force_update, using, update_fields)
        # print("self.category : ", self.category.all())

    def save_base(self, raw=False, force_insert=False, force_update=False, using=None, update_fields=None):
        print("SAVE BASE")
        print("self : ", self.__dict__)
        super().save_base(raw, force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # print("self : ", self)
        # print("self : ", self.__dict__)
        # print("self.category : ", self.category)
        # if self.category:
        #     print("self.category : ", self.category)
        #     self.category.del_all_counter()
            # raise Exception("")
            # cats = self.category.all()
            # for cat in cats:
            #     print("cat FROM DELETE: ", cat)
            #     cat.set_counter_with_parent("del")
            #
            # #REMOVE ALL RELATIONS
            # self.category.clear()


        return super().delete(using, keep_parents)

    #TODO LINK WITH SIMILAR METHOD
    # AND SERIALIZER FROM PREFERED
    def get_category(self):
        return list(self.category.values_list("name", flat=True))

    def get_peoples(self):
        return list(self.peoples.values_list("name", flat=True))

    def get_places(self):
        return list(self.places.values_list("name", flat=True))

    def get_periods(self):
        return list(self.periods.values_list("name", flat=True))

    def get_things(self):
        return list(self.things.values_list("name", flat=True))

    def add_counter(self, add=True):
        if isinstance(add, bool):
            if add:
                self.like_counter += 1
                self.save(update_fields=['like_counter'])
                return self.like_counter
            else:
                self.dislike_counter += 1
                self.save(update_fields=['dislike_counter'])
                return self.dislike_counter
        else:
            raise Exception("Choice are a bool")


    #TODO  refactor
    def get_cat_list(self):
        k = self.category.all()  # for now ignore this instance method
        print("k : ", k)
        breadcrumb = ["dummy"]
        [breadcrumb.append(cat.slug) for cat in k]
        print("breadcrumb : ", breadcrumb)
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        print("breadcrumb : ", breadcrumb)
        return breadcrumb[-1:0:-1]
