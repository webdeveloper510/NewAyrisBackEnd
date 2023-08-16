from django.db import models
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

from ayris.custom.models import (
TimestampModel,
MasterModel,
)

from django.core.exceptions import ValidationError
from io import BytesIO

# def get_images_path():
#     return os.path.join(settings.MEDIA_ROOT, 'images')
# def validate_file_extension(value):
#     ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
#     return ext

# def raise_error_file(value, valid_extensions):
#     import os
#     from django.core.exceptions import ValidationError
#     print("value : ", value)
#     print("value : ", value.instance.image.__dict__)
#     print("value : ", value.storage.__dict__)
#     print("value : ", value.__dict__)
#     ext = os.path.splitext(value.name)[1]
#     if not ext.lower() in valid_extensions:
#         raise ValidationError(f'Unsupported file extension. Only {str(valid_extensions)}')

VALID_IMG_EXT = ['jpg', 'jpeg', 'png', 'svg', 'gif']
VALID_GIF_EXT = ['gif']


def validate_image_extension(value):
    return FileExtensionValidator(allowed_extensions=VALID_IMG_EXT)(value)


def validate_gif_extension(value):
    return FileExtensionValidator(allowed_extensions=VALID_GIF_EXT)(value)

"""
TO CHECK IMAGE TYPE 
TODO REPLACE ALL FileField by this Class

TODO ADD CHECK im.verify() BEFORE check format


maybe change method with magic :
https://pypi.org/project/python-magic

"""
class ImageFieldChecker(models.ImageField):

    def to_python(self, data):
        print("TO PYTHON")
        print("data : ", data)
        f = super(ImageFieldChecker, self).to_python(data)
        print(" f : ",  f)
        if f is None:
            return None

        try:
            from PIL import Image
        except ImportError:
            import Image

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
            print("file : ", file)
        else:
            if hasattr(data, 'read'):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data['content'])
            print("file 2: ", file)
        try:
            print("IMAGE : ")
            im = Image.open(file)
            print("im : ", im)
            print("im.format : ", im.format)
            if im.format not in ('BMP', 'PNG', 'JPEG', 'GIF', 'SVG'):
                raise ValidationError("Unsupport image type. Please upload gif, bmp, png or jpeg")
        except ImportError:
            # Under PyPy, it is possible to import PIL. However, the underlying
            # _imaging C module isn't available, so an ImportError will be
            # raised. Catch and re-raise.
            raise
        except Exception: # Python Imaging Library doesn't recognize it as an image
            raise ValidationError(self.error_messages['invalid_image'])

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


# class Test(models.Model):
#
#     img = ImageFieldChecker(
#         upload_to="images"
#     )

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)

    image = ImageFieldChecker(
        upload_to="images",
        blank=False,
        validators=[validate_image_extension]
    )

    def __str__(self):
        return f"{self.title} - {self.image.name}"

    class Meta:
        abstract = True


class ImageBuild(Image):
    class Meta:
        db_table = "image_build"


# class Gif(models.Model):
#     title = models.CharField(max_length=200, blank=True, null=True)
#
#     image = ImageFieldChecker(
#         upload_to="gifs",
#         blank=False,
#         validators=[validate_gif_extension]
#     )
#
#
#     def __str__(self):
#         return f"{self.title} - {self.image.name}"
#
#     class Meta:
#         db_table = "gif"

"""
    type
    color
    matter
"""

class ObjectN(models.Model):
    name = models.CharField(
        _("Object Name"),
        max_length=30,
        # unique=True
    )

    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name



class ObjectName(ObjectN):
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    is_approuve = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "build_obj_name"
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "name"],
                name="unic_parent_and_child"
            ),
        ]

    def get_slug(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return full_path[::-1]

    def __str__(self):
        full_path = self.get_slug()
        return ' -> '.join(full_path)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        full_path = self.get_slug()
        self.slug = slugify(full_path)
        super().save(force_insert, force_update, using, update_fields)


class Shield(models.Model):

    title = models.CharField(
        _('Shield Title'),
        max_length=30,
        default=""
    )

    image = models.OneToOneField(
        ImageBuild,
        on_delete=models.CASCADE,
        default=0
    )

    def __str__(self):
        return self.title

class Banner(models.Model):

    title = models.CharField(
        _('Banner Title'),
        max_length=30,
        default=""
    )

    image = models.OneToOneField(
        ImageBuild,
        on_delete=models.CASCADE,
        default=0
    )

    def __str__(self):
        return self.title

class AlbumCategory(models.Model):
    name = models.CharField(
        _("Category Album"),
        max_length=30,
        unique=True
    )

class Album(models.Model):
    title = models.CharField(
        _("Title Album"),
        max_length=50,
    )

    image = models.ForeignKey(
        ImageBuild,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        AlbumCategory,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title if self.title else "Album has no title"

class Build(TimestampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
        related_name="build"
    )

    title = MasterModel.set_basic_field(
        models.CharField,
        'Title'
    )

    artist_name = MasterModel.set_basic_field(models.CharField, 'Artist name')

    # TODO KNOW if it's passion and type of work AND
    # ONE PER USER OR MANY

    object_name = models.ManyToManyField(
        ObjectName,
        blank=True
    )

    video_link = MasterModel.set_basic_field(
        models.URLField,
        'video name',
        max_length=50
    )

    image_link = MasterModel.set_basic_field(
        models.URLField,
        'Image Link',
        max_length=50
    )

    #TODO ADD VALIDATOR TO ALLOW ONLY RIGHT TYPE OF IMAGE
    image = models.OneToOneField(
        ImageBuild,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


    #TODO ADD VALIDATOR TO ALLOW ONLY GIF
    # gif = models.OneToOneField(
    #     Gif,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True
    # )

    live_link = MasterModel.set_basic_field(
        models.URLField,
        'Live Link',
        max_length=50
    )

    homepage_link = MasterModel.set_basic_field(
        models.URLField,
        'Homepage Link',
        max_length=50
    )

    vitea_link = MasterModel.set_basic_field(
        models.URLField,
        'Vitea Link',
        max_length=50
    )

    domus_link = MasterModel.set_basic_field(
        models.URLField,
        'Domus Link',
        max_length=50
    )

    shield = models.ForeignKey(
        Shield,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    banner = models.ForeignKey(
        Banner,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    albums = models.ManyToManyField(
        Album,
        blank=True
    )

    #TODO ADD LIMIT OF OBJECT_NAME

    def get_object_name(self):
        return self.object_name.all()

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/media_file/%s" width="150" height="150" />' % (self.image.image))
        else:
            return

    image_tag.short_description = 'Image'

    # def gif_tag(self):
    #     if self.gif:
    #         return mark_safe('<img src="/media_file/%s" width="150" height="150" />' % (self.gif.image))
    #     else:
    #         return
    #
    # gif_tag.short_description = 'Gif'


# EditCat
"""
    
class FavoriteCat
    order
    Category Or Theme
    edit_name()
"""



