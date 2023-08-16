from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
import factory
import accounts.models as accounts_model
from django_countries import countries

NETWORKS_NAME = [
    "FACEBOOK",
    "BEHANCE",
    "BLOGGER",
    "TWITTER",
    "TUMBLR",
]

CHARACTER_NAME = [
    "Elfe",
    "Gnome",
    "Witche",
    "Warlock",
    "Ovni",
    "Dragon",
    "Angel",
    "Demon"
]


class Provider(faker.providers.BaseProvider):
    def get_rdn_location(self):
        return self.random_element(countries)

    def get_a_user(self):
        email = "aaa@aaa.com"
        try:
            user = accounts_model.CustomUser.objects.get(email=email)
        except:
            raise Exception(f"Email User : {email} not exist")
        else:
            return user
        return

    def get_rdn_network_type(self):
        return self.random_element(accounts_model.NetworkName.objects.all())

    def get_rdn_character(self):
        return self.random_element(CHARACTER_NAME)

    def get_rdn_talent(self):
        return self.random_element(accounts_model.Talent.objects.all())


class ProfileFactory(factory.Factory):
    class Meta:
        model = accounts_model.Profile

    name = factory.Faker('sentence', nb_words=1)
    title = factory.Faker('sentence', nb_words=3)
    age = factory.Faker('pyint', min_value=33, max_value=999)


class SocialNetworkLinkFactory(factory.Factory):
    class Meta:
        model = accounts_model.SocialNetworkLink

    url = factory.Faker('sentence', nb_words=1)


class TalentFactory(factory.Factory):
    class Meta:
        model = accounts_model.Talent

    name = factory.Faker('sentence', nb_words=3)

class EmailProfileFactory(factory.Factory):
    class Meta:
        model = accounts_model.Email

    email = factory.Faker('email')


def create_obj(obj_class, list_name):
    class_name = obj_class.__name__
    if obj_class.objects.count() == 0:
        print(f"{class_name} CREATED")
        [obj_class.objects.create(name=name) for name in list_name]
    else:
        print(f"{class_name} WAS created")


def create_networks_type():
    create_obj(accounts_model.NetworkName, NETWORKS_NAME)


def create_character():
    create_obj(accounts_model.Character, CHARACTER_NAME)


class Command(BaseCommand):
    help = "Command information"

    def create_network_links(self, number=3, profile=None):

        for _ in range(number):
            network_name = self.fake.get_rdn_network_type()
            if not profile.social_networks.filter(network_name__name=network_name):
                network_link = SocialNetworkLinkFactory()
                network_link.network_name = network_name
                print("network_name : ", network_name)
                network_link.url = f"http://" \
                                   f"{str(network_link.url[:-1]).lower()}" \
                                   f"/{str(network_name).lower()}.com"
                network_link.profile = profile
                print("network_link : ", network_link)
                network_link.save()

    def create_talent(self, number=3, limit=7, profile=None):
        if hasattr(profile, "talents"):

            if number + profile.talents.count() <= limit:
                print(f"{str(number)} TALENTS CREATED")
                for _ in range(number):
                    t = TalentFactory()
                    t.profile = profile
                    t.save()
            else:
                print(f"TALENTS WAS created")



    def create_profile(self, user):
        if not hasattr(user, "profile"):
            print("PROFILE CREATED")

            profile = ProfileFactory()
            profile.user = user
            profile.save()
            return profile
        else:
            return user.profile


    def set_emails(self, profile, numbers):
        if profile and profile.emails.count() == 0:
            print("SET PROFILE WITH EMAILS")
            emails = [EmailProfileFactory() for _ in range(numbers)]
            for email in emails:
                email.profile = profile
            [email.save() for email in emails]

    def handle(self, *args, **kwargs):
        create_networks_type()
        create_character()

        self.fake = Faker()
        self.fake.add_provider(Provider)

        user = self.fake.get_a_user()
        print(f"User selected : {user}")
        profile = self.create_profile(user) if not user.profile else user.profile
        print("profile : ", profile)
        self.set_emails(profile, numbers=3)

        if not user.profile.character:
            caractere_name = self.fake.get_rdn_character()
            caractere = accounts_model.Character.objects.get(name=caractere_name)
            print("OLD profile.character : ", profile.character)
            profile.character = caractere
            print("NEW profile.character : ", profile.character)

        # if not profile.localisation:
        #     localisation = self.fake.get_rdn_location()
        #     profile.localisation = localisation


        profile.save()

        self.create_network_links(3, profile)

        self.create_talent(number=3, profile=profile)

        self.stdout.write(self.style.SUCCESS(f"Profile save"))
