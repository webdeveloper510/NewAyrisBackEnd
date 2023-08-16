from rest_framework import serializers

from category.serializers import (
ThingSerializer,
PeopleSerializer,
PeriodSerializer,
PlaceSerializer
)

from artworks.serializers import (
ArtWorkSerializer,
MediumSerializer,
ColorSerializer,
MatterSerializer
)

from .models import (
Period,
People,
Thing,
Place,
Style,
Profession,
UserPreference,
ArtWorkPref,
CatPref
)


#
# class ObjSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             'name',
#         )
#
#
# class PeriodSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = Period
#
#
# class ThingSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = Thing
#
#
# class PeopleSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = People
#
#
# class PlaceSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = Place
#
#
# class StyleSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = Style
#
#
# class ProfessionSerializer(ObjSerializer):
#     class Meta:
#         fields = ObjSerializer.Meta.fields
#         model = Profession

# def remove_fields(serializer_fields: tuple, name):
#     if isinstance(name, str):
#         return tuple(filter(lambda x: x != name, serializer_fields))

from machine.serializers import MenuSerializer


class CatPrefSerializer(MenuSerializer):
    pass


class ArtWorkPrefSerializer(serializers.ModelSerializer):

    # mediums = MediumSerializer(many=True)
    mediums = serializers.CharField(source="get_mediums_l")
    colors = ColorSerializer(many=True)
    matters = MatterSerializer(many=True)

    class Meta:
        fields = (
            'mediums',
            'matters',
            'colors'
        )
        model = ArtWorkPref


class UserPreferenceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email")
    # peoples = PeopleSerializer(many=True)
    # peoples = serializers.CharField(source="get_peoples_l")
    peoples = serializers.SerializerMethodField()
    things = serializers.SerializerMethodField()
    places = serializers.SerializerMethodField()
    styles = serializers.SerializerMethodField()
    professions = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()

    mediums = serializers.SerializerMethodField()
    matters = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    # categories = serializers.SerializerMethodField()
    categories = CatPrefSerializer(many=True)

    class Meta:
        fields = (
            'user',
            'categories',
            'peoples',
            'periods',
            'things',
            'places',
            'styles',
            'professions',
            'mediums',
            'colors',
            'matters'
        )

        model = UserPreference

    def get_peoples(self, obj):
        return obj.sample_method()

    def get_periods(self, obj):
        return obj.sample_method()

    def get_things(self, obj):
        return obj.sample_method()

    def get_places(self, obj):
        return obj.sample_method()

    def get_styles(self, obj):
        return obj.sample_method()

    def get_professions(self, obj):
        return obj.sample_method()

    def get_mediums(self, obj):
        return obj.sample_method()

    def get_colors(self, obj):
        return obj.sample_method()

    def get_matters(self, obj):
        return obj.sample_method()

    # def get_categories(self, obj):
    #     return obj.categories

