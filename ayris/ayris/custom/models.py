from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MasterModel:

    @staticmethod
    def set_basic_field(obj, title, max_length=25):

        if obj and title:
            return obj(
                _(title),
                max_length=max_length,
                blank=True
            )

    @staticmethod
    def set_basic_integer(title):
        return models.PositiveIntegerField(
            _(title),
            default=0,
        )


class Error:
    @staticmethod
    def check_is_str(input):
        check = True if input and isinstance(input, str) else False
        if not check:
            raise Exception("IS not a string")
        return check


class Filter:
    @staticmethod
    def test(theme="Mythology", category=None, choice=None):
        print(Filter.get_all_theme())
        print(Filter.get_theme(theme))
        print(Filter.get_post_by_theme(theme))
        print(Filter.get_counter_by_theme(theme))
        print(Filter.get_all_choices())
        print(Filter.get_choices_by_theme(theme))

    @staticmethod
    def get_all_theme():
        from category.models import Theme
        return Theme.objects.all()

    @staticmethod
    def get_theme(name):
        if Error.check_is_str(name):
            themes = Filter.get_all_theme()
            return themes.get(name=name)

    @staticmethod
    def get_post_by_theme(name):
        them = Filter.get_theme(name)
        from post.models import Post

        return Post.objects.filter(
            choice__theme__name=them.name,
        )

    @staticmethod
    def get_counter_by_theme(name):
        posts = Filter.get_post_by_theme(name)

        return posts.count()


    @staticmethod
    def get_all_counter_by_theme():
        pass

    @staticmethod
    def get_all_choices():
        from category.models import ThemeChoice
        return ThemeChoice.objects.all()

    @staticmethod
    def get_choices_by_theme(them_name):
        them = Filter.get_theme(them_name)
        return them.choices.all()
    #
    @staticmethod
    def get_post_by_choice(theme, name, cat):
        from post.models import Post
        # raise Exception(cat)
        if Error.check_is_str(theme) and Error.check_is_str(name) and isinstance(cat, list):
            return Post.objects.filter(
                choice__theme__name=theme,
                category__in=cat,
                choice__choice=name
            )
            posts = Post.objects.filter(
                choice__theme__name=theme,
                choice__choice=name
            )
            for p in posts:
                print("p : ", p)
                print("p.category.all() : ", p.category.all())
                print("p.choice : ", p.choice)
                print("-------------------------------------")


            return posts

    @staticmethod
    def get_count_by_theme_choice(theme, name, cat):
        return Filter.get_post_by_choice(theme, name, cat).count()
