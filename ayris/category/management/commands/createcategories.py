from django.core.management.base import BaseCommand
from django.core import management

import category.models as cat_model

MYTH_CAT = [
    "Egyptian",
    "Rome",
    "Christian",
    "Indian",
    "Scandinavian",
    "Native American",
    "Etheric"
]

class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        them_myth = None
        try:
            them_myth = cat_model.Theme.objects.get(name="Mythology")
        except Exception as e:
            print("e : ", e)

            try:
                management.call_command('createtheme')
            except Exception as e:
                raise Exception("ALREaDY Create", e)
        finally:
            # print("cat_myth : ", them_myth)
            if not them_myth:
                them_myth = cat_model.Theme.objects.get(name="Mythology")
            theme_name = them_myth.name
            for cat_str in MYTH_CAT:
                cat_nam = cat_str + " " + theme_name
                print("cat_nam : ", cat_nam)
                print("them_myth : ", them_myth)
                try:
                    sub_cat = cat_model.Category(
                        name=cat_nam,
                        theme=them_myth
                    )
                    sub_cat.save()


                except Exception as e:
                    print(f"{theme_name} -> {cat_nam} ALREADY EXIST")
                    print("e : ", e)

            counter = cat_model.Category.objects.filter(theme=them_myth).count()
            self.stdout.write(self.style.SUCCESS(f"Number of post: {counter}"))




