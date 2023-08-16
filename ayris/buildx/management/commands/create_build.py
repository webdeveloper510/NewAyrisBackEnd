from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
import factory
import accounts.models as accounts_model
import buildx.models as build_model

OBJ_NAME_LIST = [
    "Artist",
    "Musicien",
    "Sculptur",
    "Designer"
]

OBJ_NAME_CAT = [
    "EMPIRE",
    "MEDIUM",
]

OBJ_EMPIRE = [
    "CHURCHES",
    "CHURCH ENTIERIOR ALTAR PIECE",
    "TEMPLE",
    "CITY HALLS",
    "LAMP",
    "VASE"
]

OBJ_MEDIUM = [
    "ENGRAVING",
    "PAINTING",
    "MOZAIC",
    "INK ON CANVAS",
    "OIL PAINT ON CANVAS",
    "OIL PAINT ON HARDBOARD",
    "CHARCOAL DRAWING",
]

def create_obj_name_cat(is_approuve):
    if build_model.ObjectName.objects.count() < len(OBJ_NAME_CAT):
        obj_cat = build_model.ObjectName.objects
        [obj_cat.create(name=obj, is_approuve=is_approuve) for obj in OBJ_NAME_CAT]

def create_obj(is_approuve):
    if build_model.ObjectName.objects.count() > 0:
        objs_cat = build_model.ObjectName.objects.filter(parent__isnull=True)
        obj_name = build_model.ObjectName.objects
        for obj_cat in objs_cat:
            if obj_cat.name == "EMPIRE":
                for obj_emp in OBJ_EMPIRE:
                    print(f"{obj_cat.name} -> {obj_emp} CREATED")
                    obj_name.create(
                        name=obj_emp,
                        is_approuve=is_approuve,
                        parent=obj_cat
                    )
            elif obj_cat.name == "MEDIUM":
                for obj_med in OBJ_MEDIUM:
                    print(f"{obj_cat.name} -> {obj_med} CREATED")
                    obj_name.create(
                        name=obj_med,
                        is_approuve=is_approuve,
                        parent=obj_cat
                )


class Provider(faker.providers.BaseProvider):

    def get_a_user(self):
        return accounts_model.CustomUser.objects.get(email="aaa@aaa.com")

    def get_rdn_network_type(self):
        return self.random_element(accounts_model.NetworkName.objects.all())

    def get_a_object_name(self):
        return self.random_element(OBJ_NAME_LIST)

    def get_a_object_name(self):
        obj_cat = build_model.ObjectName.objects.all()
        limit = self.random_int(1, 3)
        return self.random_choices(obj_cat, limit)

    def get_rdn_image(self):
        return self.random_element(build_model.Image.objects.all())

    def get_rdn_gif(self):
        return self.random_element(build_model.Gif.objects.all())

class TitleFactory(factory.Factory):
    class Meta:
        pass
    title = factory.Faker('sentence', nb_words=2)

class BannerFactory(TitleFactory):
    class Meta:
        model = build_model.Banner


class ShieldFactory(TitleFactory):
    class Meta:
        model = build_model.Shield

class AlbumFactory(TitleFactory):
    class Meta:
        model = build_model.Album

class BuildFactory(factory.Factory):
    class Meta:
        model = build_model.Build

    # "object_name": null,
    # "image": "images/Ayris_Diagram.vpd_MoMHGOv.png",
    # "gif": null,

    title = factory.Faker('sentence', nb_words=2)
    artist_name = factory.Faker('sentence', nb_words=2)
    video_link = factory.Faker('url')
    image_link = factory.Faker('image_url')
    live_link = factory.Faker('url')
    vitea_link = factory.Faker('url')
    homepage_link = factory.Faker('url')
    domus_link = factory.Faker('url')
    # age = factory.Faker('pyint', min_value=33, max_value=999)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        self.fake = Faker()
        self.fake.add_provider(Provider)



        build_model.Build.objects.all().delete()
        build_model.Banner.objects.all().delete()
        build_model.Shield.objects.all().delete()
        build_model.Album.objects.all().delete()

        user = self.fake.get_a_user()
        print("user : ", user)
        is_approuve = user.is_superuser

        # CREATE OBJ_NAME CAT
        create_obj_name_cat(is_approuve)
        create_obj(is_approuve)
        # print("getattr() : ", hasattr(user, 'build'))
        if not hasattr(user, 'build'):
            image = self.fake.get_rdn_image()
            gif = self.fake.get_rdn_gif()
            object_name = self.fake.get_a_object_name()

            banner = BannerFactory()
            banner.image = image
            banner.save()

            shield = ShieldFactory()
            shield.image = image
            shield.save()

            album = AlbumFactory()
            album.image = image
            album.save()

            build = BuildFactory()
            build.image = image
            build.gif = gif
            build.banner = banner
            build.shield = shield
            # raise Exception(object_name)
            # build.object_name.set(object_name)

            # build.id = user.build.id
            user.build = build
            user.build.save()
            user.build.object_name.set(object_name)
            user.build.albums.set([album])

        else:
            print("user.build : ", user.build)

            # if not user.build.object_name:
            #     object_name = self.fake.get_a_object_name()
            #     print("object_name : ", object_name)
            #     obj_name = build_model.ObjectName.objects.create(name=object_name)
            #     user.build.object_name = obj_name
            #     print("obj_name : ", obj_name)

            user.build.save()

        self.stdout.write(self.style.SUCCESS(f"Profile save"))
