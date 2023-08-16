from django.db import models


class CatPrefManager(models.Manager):
    def get_users_by_cat(self, cat_name):
        cats = self.filter(category__name=cat_name)
        # print("cats.values('user')", cats.values('user'))
        return [c.user for c in cats]


class UserPreferenceManager(models.Manager):
    def __check__entry(self, list_name):
        list_name = [list_name] if isinstance(list_name, str) else list_name
        return (True, list_name) if isinstance(list_name, list) else (False, None)

    def get_users_by_people(self, research_names):
        check, list_name = self.__check__entry(research_names)
        print("check", check)
        print("list_name", list_name)
        if check and list_name:
            peoples = self.filter(peoples__name__in=list_name).distinct()
            print("peoples", peoples)
            # # print("cats.values('user')", cats.values('user'))
            return [p.user for p in peoples]
        else:
            raise Exception(f"{research_names} is not a list")
    # Period,
    # People,
    # Thing,
    # Place,
    # Style,
    # Profession
