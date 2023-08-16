
from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
# import random
import factory
import accounts.models as accounts_model
# import buildx.models as build_model
# import machine.models as machine_model
import category.models as category_model
import post.models as post_model

# class PostType(models.IntegerChoices):
#     __empty__ = _('(Unknown)')
#     ARTICLE = 1, _('Article')
#     GUESTBOOK = 2, _('Male')
#     POEM = 3, _('No gender')
#     PERSONNAL_ESSAY = 3, _('No gender')
#     SIMILAR_ART = 3, _('No gender')

POST_TYPE = [
    "ARTICLE",
    "GUESTBOOK",
    "POEM",
    "PERSONNAL_ESSAY",
    "SIMILAR_ART",
]

class Provider(faker.providers.BaseProvider):

    def get_a_user(self):
        # email = "cccc@cccc.com"
        email = "aaa@aaa.com"
        return accounts_model.CustomUser.objects.get(email=email)
        # return self.random_element(accounts_model.CustomUser.objects.all())

    def get_rdn_post_type(self):
        return self.random_element(post_model.PostType.objects.all())

    def reset_theme_counter(self, theme):
        theme.counter = 0
        theme.save(update_fields=["counter"])

    def get_theme(self):
        return category_model.Theme.objects.get(name="Mythology")
    
    def remove_all_post(self):
        check = post_model.Post.objects.exists()
        print("check : ", check)
        if check:
            posts = post_model.Post.objects.all()
            [post.delete() for post in posts]
            # posts.delete()
        print("REMOVE ALL POST")
        return check

    def reset_cat_counter(self):
        cats = category_model.Category.objects.all()
        for cat in cats:
            cat.counter = 0
            print(f"{cat} reset counter")
            cat.save(update_fields=['counter'])

        print("RESET ALL COUNTER")

    def get_rdn_category(self):
        # cats = category_model.Category.objects.filter(parent__isnull=False)
        cats = category_model.Category.objects.all()
        limit = self.random_int(1, 5)
        return self.random_choices(cats, limit)

    def get_rdn_choice(self, theme):
        # raise Exception(choices.all())
        return self.random_element(theme.choices.all())


    # def get_machine(self):
    #     return machine_model.Machine.objects.first()
    #
    # def create_main_cat(self):
    #     for l in LIST_MAIN_CAT:
    #         category_model.Theme.objects.create(name=l, slug=l)



class PostFactory(factory.Factory):
    class Meta:
        model = post_model.Post

    title = factory.Faker('sentence', nb_words=4)
    # description = factory.Faker('sentence', nb_words=10)
    content = factory.Faker('sentence', nb_words=100)
    slug = title


def set_post_attr(post, choice_theme):
    post.title = post.title[:-1]
    post.slug = post.title.split(' ')[0]
    post.choice = choice_theme
    return post


post_list = []


def check_post_type():
    return post_model.PostType.objects.exists()

def create_post_type():
    p_type_check = check_post_type()
    if not p_type_check:
        [post_model.PostType.objects.create(name=post_type) for post_type in POST_TYPE]
        print("post_model.PostType.objects.all() : ", post_model.PostType.objects.all())


class Command(BaseCommand):
    help = "Command information"



    def set_posts(self, nb_post=5, theme=None, user=None):
        if theme and user:
            for _ in range(nb_post):
                choice_theme = self.fake.get_rdn_choice(theme)
                post_type = self.fake.get_rdn_post_type()
                post = set_post_attr(PostFactory(), choice_theme)
                post.post_type = post_type
                post.user = user
                post_list.append(post)

            for post in post_list:
                post.save()
                categories = self.fake.get_rdn_category()
                # raise Exception("categories[0].theme : ", categories[0].theme)
                # choice_theme = self.fake.get_rdn_choice_theme()
                for cat in categories:
                    print("cat : ", cat)
                    cat.add_counter()
                    # cat.update(counter=+1)
                    print("cat.parent : ", cat.parent)
                    # if cat.parent and not cat.parent.parent:
                    #     cat.parent.add_counter()
                        # cat.parent.save(update_fields=['counter'])
                    # print("----------------------------------")
                    # cat.save(update_fields=['counter'])

                    theme.add_counter()
                    # theme.save(update_fields=['counter'])

                    # cat.theme.
                    post.category.add(cat)
                    print("post : ", post)
        else:
            raise Exception("No main Theme")

    # def add_arguments(self, parser):
    #     parser.add_argument('-c', '--clean', help='Define --clean')

    def handle(self, *args, **kwargs):
        # raise Exception("")
        # create_post_type()

        self.fake = Faker()
        self.fake.add_provider(Provider)

        create_post_type()

        check = self.fake.remove_all_post()

        theme = self.fake.get_theme()

        self.fake.reset_theme_counter(theme)
        self.fake.reset_cat_counter()

        user = self.fake.get_a_user()
        self.set_posts(nb_post=1, theme=theme, user=user)


        self.stdout.write(self.style.SUCCESS(f"Number of post: {len(post_list)}"))
