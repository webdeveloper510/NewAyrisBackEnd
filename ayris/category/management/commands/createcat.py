from django.core.management.base import BaseCommand

import category.models as cat_model

Cat_obj = cat_model.Category.objects
People_obj = cat_model.People.objects
Thing_obj = cat_model.Thing.objects
Period_obj = cat_model.Period.objects
Place_obj = cat_model.Place.objects
Profession_obj = cat_model.Profession.objects
Style_obj = cat_model.Style.objects

LIST_CAT_NAME = [
    "year",
    "Era/Style",
    "Location",
    "Medium",
    "Philosophy",
    "Mythology",
    "Empresses",
    "Dream Engine",
    "Etherith",
    "Banners",
    "Heaven",
    "Music",
    "Library",
    "Court",
    "Empire",
    "Army",
    "Market",
    "Treasury"
]

MYTH_CAT = [
    "Egyptian",
    "Rome",
    "Christian",
    "Indian",
    "Scandinavian",
    "Native American",
    "Etheric"
]

PEOPLES = [
    "Isis",
    "Thor",
    "Horus",
    "Amon",
    "Toutankamon",
    "Seth"
]


THINGS = [
    "CHURCHES",
    "CHURCH ENTIERIOR ALTAR PIECE",
    "TEMPLE",
    "CITY HALLS",
    "LAMP",
    "VASE"
]

PERIODS = [
    "Renaissance",
    "Neolithic",
    "Gold Age",
    "Iron Age",
    "Stone Age",
    "Unknow"
]

PLACES = [
    "Thebes",
    "Amonpolis",
    "Necropolis",
    "Pyramid de gyze",
    "Nil"
]

STYLES = [
    "Renaissance",
    "Gothic",
    "Contemporain",
    "New age",
]

PROFESSIONS = [
    "Artist",
    "Web Developper",
    "Sculpteur",
    "Drawer",
    "Designer",
    "President lol",
    "Cops",
]

def create_profession(list_name=None):
    Profession_obj.all().delete()
    if list_name and not Profession_obj.exists():
        for l in list_name:
            Profession_obj.create(name=l)

def create_style(list_name=None):
    Style_obj.all().delete()
    if list_name and not Style_obj.exists():
        for l in list_name:
            Style_obj.create(name=l)


def create_people(list_name=None):
    People_obj.all().delete()
    if list_name and not People_obj.exists():
        for l in list_name:
            People_obj.create(name=l)

def create_things(list_name=None):
    Thing_obj.all().delete()
    if list_name and not Thing_obj.exists():
        for l in list_name:
            Thing_obj.create(name=l)

def create_place(list_name=None):
    Place_obj.all().delete()
    if list_name and not Place_obj.exists():
        for l in list_name:
            Place_obj.create(name=l)

def create_period(list_name=None):
    Period_obj.all().delete()
    if list_name and not Period_obj.exists():
        for l in list_name:
            Period_obj.create(name=l)


def create_cat(list_name=None, cat_parent=None):
    if Cat_obj.count() >= len(LIST_CAT_NAME) + len(MYTH_CAT):
        Cat_obj.all().delete()
        print("DELETE")
    # print("Cat_obj.count() : ", Cat_obj.count())
    # print("len(list_name) : ", len(list_name))
    # print("5555555555555555555555555555")
    # Create main Category
    if list_name and Cat_obj.count() < len(list_name):
        for l in list_name:
            Cat_obj.create(name=l)
            print(f"{l} was CREATE")

    # print("Cat_obj.count() : ", Cat_obj.count())
    # print("len(list_name) : ", len(list_name))
    # print("666666666666666666666666")
    # Create childrens Category
    if list_name and cat_parent:
        print("INNNNN")
        for l in list_name:
            print("l : ", l)
            print(f"{cat_parent.name} > {l} WAS CREATED")
            t = cat_model.Category(
                name=l,
                parent=cat_parent
            ).save()
            print("t : ", t)
            if hasattr(t, "slug"):
                print("t.slug : ", t.slug)

def get_cat(name):
    return Cat_obj.get(name=name)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        create_cat(LIST_CAT_NAME)
        myth_cat = get_cat("Mythology")
        print("myth_cat : ", myth_cat)

        create_cat(MYTH_CAT, myth_cat)
        create_people(PEOPLES)
        create_period(PERIODS)
        create_place(PLACES)
        create_things(THINGS)
        create_profession(PROFESSIONS)
        create_style(STYLES)

        sub_cat = get_cat("Egyptian")
        print("sub_cat : ", sub_cat)

        self.stdout.write(self.style.SUCCESS(f"Number of post: {len(LIST_CAT_NAME)}"))
        
        

