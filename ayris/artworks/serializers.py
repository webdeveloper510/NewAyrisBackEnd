from rest_framework import serializers

from .models import (
Medium,
Matter,
Color,
ArtWork
)


class ArtObjSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
        )


class MediumSerializer(ArtObjSerializer):
    class Meta:
        fields = ArtObjSerializer.Meta.fields
        model = Medium


class MatterSerializer(ArtObjSerializer):
    class Meta:
        fields = ArtObjSerializer.Meta.fields
        model = Matter


class ColorSerializer(ArtObjSerializer):
    class Meta:
        fields = ArtObjSerializer.Meta.fields
        model = Color


class ArtWorkSerializer(serializers.ModelSerializer):

    mediums = MediumSerializer(many=True)
    matters = MatterSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        fields = (
            'name',
            'mediums',
            'matters',
            'colors'
        )

        model = ArtWork

