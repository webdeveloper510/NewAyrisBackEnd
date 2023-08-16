from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import (
CustomUser,
Profile,
Email,
Talent,
NetworkName,
SocialNetworkLink,
)

from buildx.serializers import BuildSerializer
from machine.serializers import (
MenuSerializer, CircleSerializer
)

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            # 'id',
            'email',
        )

        model = Email


class TalentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            # 'id',
            'name',
        )

        model = Talent


class NetworkNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = NetworkName


class SocialNetworkLinkSerializer(serializers.ModelSerializer):
    social_type = serializers.CharField(source='get_social_type')

    class Meta:
        fields = (
            'social_type',
            'url'
        )

        model = SocialNetworkLink
#
# class GuestBookSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             ''
#         )


class ProfileSerializer(serializers.ModelSerializer):
    # emails = serializers.RelatedField(source='emails', read_only=True)

    circle_member = CircleSerializer()

    emails = EmailSerializer(
        many=True,
    )
    talents = TalentSerializer(
        many=True,
    )
    social_networks = SocialNetworkLinkSerializer(
        many=True,
    )

    # localisation = serializers.CharField(source='get_localisation')
    gender = serializers.CharField(source='get_gender')
    character = serializers.CharField(source='get_character')
    spiritual_name = serializers.CharField(source='name')
    spiritual_title = serializers.CharField(source='title')
    guest_book = serializers.CharField(source='get_guest_book')

    class Meta:
        fields = (
            'spiritual_name',
            'spiritual_title',
            'circle_member',
            'gender',
            'guest_book',
            'character',
            'country',
            'city',
            'age',
            'talents',
            'emails',
            'social_networks'
        )

        model = Profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    build = BuildSerializer()
    menu = MenuSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'menu',
            'profile',
            'build'
        )
        model = CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # print(token)
        # Add custom claims
        token['fav_color'] = "coucou"
        print(token.__dict__)
        return token


class RegisterUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'password',
            'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        print("self :", self)
        password = validated_data.pop('password', None)
        # if all fields are the same
        # user = self.Meta.model(**validated_data)

        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        print("password :", password)

        user.set_password(password)
        user.save()

        return user