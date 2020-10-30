from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customers, Stars, Users, Ratings, Orders, Categories, Avatars, Videos, \
    Congratulations, Likes, MessageChats


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatars
        fields = ('username', 'image')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ('username', 'video_hi')


class CongratulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congratulations
        fields = ('star_id', 'video_con', 'order_id')


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'phone', 'email', 'password', 'avatar')


class ProfileCustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )

    class Meta:
        model = Customers
        fields = ('id', 'username', 'phone', 'email', 'avatar', 'first_name', 'last_name', 'date_of_birth', )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.phone = validated_data.get('email ', instance.email)
        instance.save()
        return instance


class ProfileStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = ('id', 'username', 'phone', 'email', 'avatar', 'first_name', 'last_name', )


class CustomerSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки даных Заказчиков
    Добавлены валидоры на создание и обновление основных полей при регистрации
    Переопределен меотод create
    """
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Customers
        fields = ('id', 'username', 'phone', 'email', 'password', 'date_of_birth', 'is_star')

    def create(self, validated_data):
        customer = Customers(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth']
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer


class StarSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки данных звезд
    Добавлены валидоры на создание и обновление основных полей при регистрации
    Переопределены методы create и update
    """

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    price = serializers.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Stars
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'phone', 'description', 'email', 'price',
                  'cat_name_id', 'profession', 'rating', 'is_star', 'days')

    def create(self, validated_data):
        star = Stars(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            price=validated_data['price'],
            cat_name_id=validated_data['cat_name_id'],
            rating=validated_data['rating'],
            is_star=validated_data['is_star']
        )
        star.set_password(validated_data['password'])
        star.save()
        return star

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки Рейтингов
    """

    class Meta:
        model = Ratings
        fields = ('rating', 'adresat', 'adresant')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'cat_name', 'cat_photo')


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки Заказов
    переопределен метод update для обновление статуса заказа
    """

    class Meta:
        model = Orders
        fields = ('id', 'customer_id', 'star_id', 'payment_id', 'order_price',
                  'by_date', 'by_time', 'for_whom', 'comment', 'status_order')

    def update(self, instance, validated_data):
        instance.price = validated_data.get('order_price', instance.price)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Customers
        fields = ('username', 'phone', 'email', 'password', 'date_of_birth', 'is_star', 'token', 'register')

    def create(self, validated_data):
        return Customers.objects.create_user(**validated_data)


class RegistrationStarSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Stars
        fields = ('username', 'phone', 'email', 'password', 'price','rating',
                  'cat_name_id', 'description', 'profession', 'is_star', 'token', 'register')

    def create(self, validated_data):
        return Stars.objects.create_user(**validated_data)


class MessageChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageChats
        fields = ('from_user', 'star_id', 'cust_id', 'message', 'message_id', )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ('star_id', 'cust_id', )


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Для входа в систему требуется адрес электронной почты.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Для входа в систему требуется пароль.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты и паролем не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь был деактивирован.'
            )

        return [{
            'token': user.token,
        }]
