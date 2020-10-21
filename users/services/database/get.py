from ...models import Customers, Stars, Ratings, Orders, Users, Categories
from ...models import Avatars, Videos, Congratulations, CatPhoto, YandexUsers
from ...serializers import LoginSerializer, UserSerializer, RegistrationSerializer, CategorySerializer
from ...serializers import CustomerSerializer, StarSerializer, RatingSerializer, OrderSerializer, AvatarSerializer
from ...serializers import VideoSerializer, CongratulationSerializer, ProfileCustomerSerializer, ProfileStarSerializer


def start_by_id(**kwargs):
    stars_set = Stars.objects.get(kwargs)
    serializer_class = StarSerializer(stars_set)
    json = serializer_class.data
    return json


def star_list():
    stars_list = Stars.objects.all()
    serializer = StarSerializer(stars_list, many=True)
    json = serializer.data
    return json


def star_by_cat_id(**kwargs):
    stars_set = Stars.objects.filter(kwargs)
    serializer_class = StarSerializer(stars_set, many=True)
    json = serializer_class.data
    return json

def avatars_all():
    avatar_set = Avatars.objects.all()
    serial_avatar = AvatarSerializer(avatar_set, many=True)
    avatar_data = serial_avatar.data
    return avatar_data

def rating(**kwargs):
    queryset = Ratings.objects.filter(kwargs)
    serializtor = RatingSerializer(queryset, many=True)
    json = serializtor.data
    return json