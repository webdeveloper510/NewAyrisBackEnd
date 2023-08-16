from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
import factory
import accounts.models as accounts_model

#
# class Provider(faker.providers.BaseProvider):
#
#     def get_a_user(self):
#         return self.random_element(accounts_model.CustomUser.objects.all())
#

class UserFactory(factory.Factory):
    class Meta:
        model = accounts_model.CustomUser

    username = factory.Faker('sentence', nb_words=1)
    email = "cccc@cccc.com"


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        # fake = Faker()
        # fake.add_provider(Provider)
        user = UserFactory()
        user.save()

        self.stdout.write(self.style.SUCCESS(f"User save"))
