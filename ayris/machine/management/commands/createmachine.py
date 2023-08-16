
from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
import random
import factory

import accounts.models as accounts_model
import buildx.models as build_model
import machine.models as machine_model
import category.models as category_model

menu_user_order = []

class Provider(faker.providers.BaseProvider):

    def get_a_user(self):
        return self.random_element(accounts_model.CustomUser.objects.filter(email="aaa@aaa.com"))
        # return self.random_element(accounts_model.CustomUser.objects.all())

    def get_machine(self):
        return machine_model.Machine.objects.get(name="Ayris Machine")
    
    def get_rdn_menu_theme(self, len_choice, limit=None):
        # nb = self.random_element(menu_user_order)
        data = random.sample(menu_user_order, len_choice)
        return data if not limit else data[:limit] if isinstance(limit, int) else None



class NewsFactory(factory.Factory):
    class Meta:
        model = machine_model.New

    text = factory.Faker('sentence', nb_words=10)


class ManifestoFactory(factory.Factory):
    class Meta:
        model = machine_model.Manifesto

    title = factory.Faker('sentence', nb_words=10)
    text = factory.Faker('sentence', nb_words=500)

class ManualFactory(ManifestoFactory):
    class Meta:
        model = machine_model.Manual



def get_all_main_cat():
    return category_model.MainCategory.objects.all()

def get_all_cat_for_user():
    return category_model.Category.objects.all()

def get_basic_menu():
    return machine_model.MenuCategory.objects.all()

def set_menu_order(machine):
    categories = get_all_main_cat()
    categories_count = categories.count()
    menu_cat = get_basic_menu()
    menu_cat_count = menu_cat.count()

    if categories_count == 0 and menu_cat_count == 0:
        if categories_count != menu_cat_count:
            [machine_model.MenuCategory.objects.create(
                machine=machine,
                category=cat
            ) for cat in categories]



class Command(BaseCommand):
    help = "Command information"
    rdn = []

    def set_menu_for_user(self, user, machine, limit=None):
        print("user : ", user)

        machine_model.MenuCategoryUser.objects.all().delete()
        menu_user = machine_model.MenuCategoryUser.objects.all()
        menu = get_basic_menu()
        print("menu_user : ", menu_user)
        if menu_user.count() == 0 and machine:
            print("menu_user : ", menu_user)
            all_cat = get_all_cat_for_user()
            count_cat = all_cat.count()
            [menu_user_order.append(nb) for nb in range(count_cat)]
            print("count_cat : ", count_cat)
            print("menu_user_order : ", menu_user_order)
            rdn = self.fake.get_rdn_menu_theme(count_cat, limit)
            print("rdn : ", rdn)

            print("menu_user_order : ", menu_user_order)
            print("len(rdn) : ", len(rdn))

            [machine_model.MenuCategoryUser.objects.create(
                order=rdn[ixd],
                machine=machine,
                category=all_cat[nb],
                user=user
            ) for ixd, nb in enumerate(rdn)]
            print("menu_user.count() : ", menu_user.count())
            print("menu.count() : ", menu.count())
            print("menu_user.count() != menu.count() : ", menu_user.count() != menu.count())

        if menu_user.count() != menu.count():
            diff = menu.count() - menu_user.count()
            index = 0
            print("menu_user.count() : ", menu_user.count())
            print("menu.count() : ", menu.count())
            print("diff : ", diff)
            print("rdn : ", rdn)
            print("menu_user_order : ", menu_user_order)
            if rdn and menu_user_order:
                for rdn_idx in rdn:
                    print(f"{rdn_idx} remove: ")
                    menu_user_order.remove(rdn_idx)
                print("new menu_user_order : ", menu_user_order[:diff])
                rest_of_idx_menu = menu_user_order[:diff]
                all_cat = category_model.Category.objects.all()
                [machine_model.MenuCategoryUser.objects.create(
                    machine=machine,
                    category=all_cat[idx],
                    user=user
                ) for idx in rest_of_idx_menu]

    def create_machine(self, name):
        machine = machine_model.Machine.objects.create(name=name)
        return machine

    def create_news(self, number, machine):
        if machine_model.New.objects.count() <= number:
            new_count = machine_model.New.objects.filter(machine=machine).count()
            print("CREAte NEWS")
            for _ in range(number):
                new = NewsFactory()
                count = new_count + _
                new.text = f"new : {str(count)} - {new.text}"
                new.machine = machine
                new.save()
            print(f"{number} was create")

    def create_manifesto(self, machine):
        print("machine.manifesto : ", machine.manifesto)
        if not machine.manifesto:
            manifesto = ManifestoFactory()
            manifesto.save()
            print("manifesto : ", manifesto)
            machine.manifesto = manifesto
            machine.save()

    def create_manual(self, machine):
        print("machine.manual : ", machine.manual)
        if not machine.manual:
            manual = ManualFactory()
            manual.save()
            print("manual : ", manual)
            machine.manual = manual
            machine.save()

    def handle(self, *args, **kwargs):
        self.fake = Faker()
        self.fake.add_provider(Provider)
        user = self.fake.get_a_user()
        machine = None
        print("-----------")
        try:
            machine = self.fake.get_machine()
        except:
            machine = self.create_machine("Ayris Machine")
        else:
            print("machine : ", machine)
            self.create_news(5, machine)
        finally:
            if machine:
                self.create_manifesto(machine)
                print("machine.manifesto : ", machine.manifesto)
                self.create_manual(machine)
                print("machine.manual : ", machine.manual)
                set_menu_order(machine)
                self.set_menu_for_user(user, machine, limit=9)

