from rest_framework import serializers

from .models import (
Build,
ImageBuild,
ObjectName,
Album,
Shield,
Banner
)

class Generic(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title',
            'image'
        )
        model = None

class ObjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = ObjectName

class ImageSerializer(Generic):
    class Meta(Generic.Meta):
        model = ImageBuild

class GenericImageSerializer(Generic):
    image = ImageSerializer()
    class Meta(Generic.Meta):
        pass

class AlbumSerializer(GenericImageSerializer):
    class Meta(Generic.Meta):
        model = Album

class ShieldSerializer(GenericImageSerializer):
    class Meta(Generic.Meta):
        model = Shield

class BannerSerializer(GenericImageSerializer):
    class Meta(Generic.Meta):
        model = Banner

class BuildSerializer(serializers.ModelSerializer):
    # object_name = serializers.CharField(source='get_object_name')
    object_name = ObjectNameSerializer(many=True)
    image = ImageSerializer()
    shield = ShieldSerializer()
    banner = BannerSerializer()
    albums = AlbumSerializer(many=True)
    # image = serializers.CharField(source='image.image')
    # gif = serializers.CharField(source='gif.image')
    class Meta:
        fields = (
            'id',
            'title',
            'object_name',
            'artist_name',
            'video_link',
            'image_link',
            'image',
            'live_link',
            'homepage_link',
            'vitea_link',
            'domus_link',
            'albums',
            'shield',
            'banner'
        )

        model = Build


