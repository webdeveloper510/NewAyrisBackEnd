from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField

from .manager import (
CustomUserManager,
ProfileManagerQuerySet
)
from ayris.custom.models import (
TimestampModel,
MasterModel
)

# from machine.models import Circle

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('user name'), max_length=30, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        db_table = "account"
        verbose_name = "user"

    def __str__(self):
        return self.email


class GenderType(models.IntegerChoices):
    __empty__ = _('(Unknown)')
    FEMALE = 1, _('Female')
    MALE = 2, _('Male')
    NO = 3, _('No gender')


class Character(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )

    class Meta:
        db_table = "profile_character"

    def __str__(self):
        return self.name


class SearchParam(models.Model):
    is_show_picture = models.BooleanField(
        default=False
    )
    is_show_within_frame = models.BooleanField(
        default=False
    )


class Country(models.Model):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    iso2 = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    iso3 = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    flag = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(models.Model):
    city = models.CharField(max_length=50)

    city_ascii = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cities"
    )

    def __str__(self):
        return self.city_ascii

    class Meta:
        ordering = ["city"]




class Profile(TimestampModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        null=True
    )

    name = models.CharField(
        _('spiritual name'),
        max_length=25,
        blank=True
    )

    title = models.CharField(
        _('spiritual title'),
        max_length=25,
        blank=True
    )

    """
    PositiveSmallIntegerField STORE only .values and not .names of IntegerChoices.choices
    """
    gender = models.PositiveSmallIntegerField(
        _('spiritual gender'),
        choices=GenderType.choices,
        default=GenderType.NO
    )

    # TODO KNOW IF ONLY ONE OR MORE SPECIFIC CHAR
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    #TODO LINKED COUNTRY AND CITY
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    age = models.PositiveSmallIntegerField(
        _('spiritual age'),
        null=True
    )

    search_param = models.OneToOneField(
        SearchParam,
        on_delete=models.CASCADE,
        null=True
    )

    circle_member = models.ForeignKey(
        "machine.Circle",
        on_delete=models.CASCADE,
        null=True,
        default=0
    )

    # guest_book = models.ManyToManyField(
    #     "accounts.CustomUser",
    #     blank=True,
    #     related_name="guest_book"
    # )


    objects = models.Manager.from_queryset(ProfileManagerQuerySet)()

    # TODO CHECK RIGHT VALUE FOR GENRE
    # TODO ADD CONSTRAINTS FOR COUNTRY AND CITY
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(gender__in=GenderType.values),
                name="%(app_label)s_%(class)s_gender_valid"
            ),
            # models.UniqueConstraint(
            #     fields=["user", "guest_book"],
            #     name="unic_user"
            # ),

        ]

    def __str__(self):
        return f"Profile : {self.user.username} "

    def get_gender(self):
        return self.get_gender_display()

    def get_character(self):
        return self.character

    def get_guest_book(self):
        return list(self.guest_book.values("profile__user__email"))

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.search_param = SearchParam.objects.create()
        instance.profile.save()


class GuestBook(models.Model):
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='guest_book',
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return str(self.user_profile) + " - " + str(self.profile)

    class Meta:
        db_table = "guest_book"
        constraints = [
            models.UniqueConstraint(
                fields=["user_profile", "profile"],
                name="unic_profile_guestbook"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(user_profile=models.F("profile")),
            ),

        ]


class Email(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='emails'
    )

    email = models.EmailField(max_length=70, unique=True)


    # TODO LIMIT OF 3 (including the main mail)
    class Meta:
        db_table = "profile_email"

    def __str__(self):
        return self.email



class Talent(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='talents'
    )

    name = models.CharField(max_length=50)

    class Meta:
        db_table = "profile_talent"

    def __str__(self):
        return self.name

    # TODO ASK HOW MANY MAX
    # TODO CONSTRAINT NUMBER OF TALENTS
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("SAVE")
        print("using : ", using)
        print("update_fields : ", update_fields)
        # print("self.profile.talents.count() : ", self.profile.talents.count())
        if self.profile.talents.count() <= 7:
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise Exception("NO MORE THEN 7 TALENTS")


class NetworkName(models.Model):

    name = models.CharField(max_length=35, unique=True)

    # class Meta:
    #     db_table = "SocialType"

    def __str__(self):
        return self.name


class SocialNetworkLink(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="social_networks",
        default=1
    )

    network_name = models.ForeignKey(
        NetworkName,
        on_delete=models.CASCADE,
        related_name="social_networks",
        default=1
    )

    url = MasterModel.set_basic_field(
        models.URLField,
        'social url',
        max_length=50
    )


    """
    CONTRAINTS TO SET ONLY ONE TYPE OF NETWORK_NAME BY PROFILE
    """
    class Meta:
        db_table = "profile_social__net_links"
        constraints = [
            models.UniqueConstraint(fields=["network_name", "profile"], name="unic_network_name"),
        ]

    def __str__(self):
        return f"{self.network_name} : {self.url}"

    @property
    def get_social_type(self):
        return self.network_name


class CustomToken(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True
    )

    refresh = models.TextField()

    jti = models.CharField(
        max_length=25,
        blank=True
    )

    exp = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
