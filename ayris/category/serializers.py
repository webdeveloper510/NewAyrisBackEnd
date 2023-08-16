from rest_framework import serializers

from .models import (
Category,
People,
Place,
Period,
Thing,
)


class NameCatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'counter'
        )



class MenuCategorySerializer(NameCatSerializer):
    class Meta:
        fields = NameCatSerializer.Meta.fields
        model = Category


class PeopleSerializer(NameCatSerializer):
    class Meta:
        fields = NameCatSerializer.Meta.fields
        model = People


class PlaceSerializer(NameCatSerializer):
    class Meta:
        fields = NameCatSerializer.Meta.fields
        model = Place


class ThingSerializer(NameCatSerializer):
    class Meta:
        fields = NameCatSerializer.Meta.fields
        model = Thing


class PeriodSerializer(NameCatSerializer):
    class Meta:
        fields = NameCatSerializer.Meta.fields
        model = Period


class CommonSerializer(serializers.ModelSerializer):
    peoples = PeopleSerializer(many=True)
    things = ThingSerializer(many=True)
    periods = PeriodSerializer(many=True)
    places = PlaceSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'slug',
            'counter',
            'peoples',
            'things',
            'periods',
            'places',

        )


class CatSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = Category


class CategorySerializer(CatSerializer):
    children = CatSerializer(many=True)
    parent = CatSerializer()

    class Meta:
        fields = CatSerializer.Meta.fields + (
            'parent',
            'description',
            'children',
        )

        model = Category
#
# class CatAndChildrenSerializer(serializers.ModelSerializer):
#     theme = ThemeSerializer()
#
#     children = CatSerializer(many=True)
#
#     class Meta:
#         fields = (
#             'id',
#             'name',
#             'theme',
#             'children',
#         )
#
#         model = Category
