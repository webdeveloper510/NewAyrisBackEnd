from rest_framework import serializers

from .models import (
Counter,
Machine,
New,
Config,
Template,
MenuCategory,
Circle
)


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            # 'machine',
            # 'id',
            'text',
        )
        model = New


class TemplateSerializer(serializers.ModelSerializer):
    # path = serializers.CharField(source='get_path')

    class Meta:
        fields = (
            'name',
            # 'path'
        )
        model = Template


class ConfigSerializer(serializers.ModelSerializer):
    template = TemplateSerializer()

    class Meta:
        fields = (
            'template',
            'limit_by_collumn'
        )
        model = Config


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            # 'id',
            'visitor_counter',
            'past_counter',
            'future_counter'
        )

        model = Counter

class CatForMenu(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name'
        )


class MenuSerializer(serializers.ModelSerializer):
    cat_id = serializers.CharField(source="category.id")
    cat_name = serializers.CharField(source="category.__str__")
    cat_slug = serializers.CharField(source="category.slug")

    class Meta:
        fields = (
            'order',
            'cat_id',
            'cat_name',
            'cat_slug'
        )

        model = MenuCategory

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'circle_number',
            'circle_name',
            'circle_type'
        )

        model = Circle

class MachineSerializer(serializers.ModelSerializer):
    counter = CounterSerializer()
    news = NewSerializer(many=True)
    config = ConfigSerializer()
    menu = MenuSerializer(many=True)
    circles = CircleSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'counter',
            'menu',
            'circles',
            'config',
            'manifesto',
            'manual',
            'news'
        )
        model = Machine

    def create(self, validated_data):
        counter = validated_data.pop('counter')
        manifesto_dict = validated_data.pop('manifesto')
        manifesto = manifesto_dict.get("text")
        # machine_name = validated_data.pop('name')
        news = validated_data.pop('news')
        # raise Exception(news)
        print("tag : ", counter)
        counter = Counter.objects.create()
        # raise Exception(manifesto)
        # manifesto, counter_manifesto = Manifesto.objects.get_or_create(text=manifesto)
        # print("manifesto, counter_manifesto : ", manifesto, counter_manifesto)
        print("validated_data : ", validated_data)
        print("counter : ", counter)
        print("manifesto : ", manifesto)

        machine = Machine.objects.create(**validated_data, counter=counter, manifesto=manifesto)
        # machine.save()
        return machine

