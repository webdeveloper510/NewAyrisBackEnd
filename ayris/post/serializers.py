from rest_framework import serializers

from .models import Post
from artworks.serializers import ArtWorkSerializer
from buildx.serializers import ImageSerializer

class PostSerializer(serializers.ModelSerializer):
    # choice = serializers.CharField(source='get_choice')
    images = ImageSerializer(many=True)
    category = serializers.CharField(source='get_category')
    peoples = serializers.CharField(source='get_peoples')
    things = serializers.CharField(source='get_things')
    places = serializers.CharField(source='get_places')
    periods = serializers.CharField(source='get_periods')
    art_work = ArtWorkSerializer()
    """
    user - post_type - 
    art_work - category - peoples - things - places - period - 
    is_approuved - like_counter
    
    #TODO LINK WITH SIMILAR METHOD
    # AND SERIALIZER FROM PREFERED
    
    
    """
    class Meta:
        fields = (
            'id',
            'title',
            # 'description',
            'slug',
            'images',
            'art_work',
            'category',
            'peoples',
            'things',
            'places',
            'periods',
            'is_approuved',
            'like_counter',
            'content',
        )

        model = Post
