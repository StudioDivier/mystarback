from math import ceil
import uuid
from PIL import Image
import simplejson
from loguru import logger
from django_rest_api_logger import APILoggingMixin
from django.shortcuts import render
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from MyStar import config

from django.forms.models import model_to_dict

from .models import Customers, Stars, Ratings, Orders, Users, Categories, Likes, VkUsers, CatPhoto, YandexUsers
from .models import Avatars, Videos, Congratulations, CatPhoto, YandexUsers, MessageChats, RequestsForm, VkUsers
from .serializers import LoginSerializer, UserSerializer, RegistrationSerializer, CategorySerializer
from .serializers import CustomerSerializer, StarSerializer, RatingSerializer, OrderSerializer, AvatarSerializer
from .serializers import VideoSerializer, CongratulationSerializer, ProfileCustomerSerializer, ProfileStarSerializer
from .serializers import LikeSerializer, MessageChatsSerializer, RegistrationStarSerializer, RequestSerializer
from .serializers import LoginSerializerOauth

from .services.auth import yandex, vk
from .services.database import put
from .services.database import get
from .services import mail

logger.add("log/debug.json", level="DEBUG", format="{time} {level} {message}", serialize=True,
           rotation="1 MB", compression="zip")


class CustomerCreate(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @logger.catch()
    def post(self, request, format='json'):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data={
                    'token': serializer.data.get('token', None),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @logger.catch()
    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            if '@' in request.data['login']:
                kwargs = {'email': request.data['login']}
            else:
                kwargs = {'username': request.data['login']}

            cust_set = Users.objects.get(**kwargs)

            try:
                ava = Avatars.objects.get(username=cust_set.avatar)
                avatar = str(ava.image)
            except Avatars.DoesNotExist:
                avatar = 'Нет фото'
            json = {
                'id': cust_set.id,
                'username': cust_set.username,
                'phone': cust_set.phone,
                'is_star': cust_set.is_star,
                'email': cust_set.email,
                'avatar': avatar,
                'token': cust_set.token
            }
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class StarCreate(APIView):
    """
    Вьюшка для создания звезды с токеном
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationStarSerializer

    @logger.catch()
    def post(self, request, format='json'):
        """
        Принимаем request Вида:
        {
            "username": "niletto",
            "phone": 9787892356,
            "email": "niletto@star.com",
            "password": 1598753426,
            "price": "15000.00",
            "rating": 0,
            "cat_name_id": "1",
            "is_star": 1
        }, где
            :param username: - ник звезды
            :param phone: - номер телефона
            :param email: - электронная почта пользователя
            :param password: - пароль (в бд храним хэш)
            :param price: - дата рождения пользователя
            :param rating: - рейтинг звезды ( по умолчанию 0)
            :param cat_name_id: - id категории
            :param is_star: - флаг звезды (1)
        1. Создаем запись в бд из данных request через сериализер
        2. Добавляем токен ьпользователю
        :return: Response 201, если запись создана. Response 400, если данные не валидные
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data={
                    'token': serializer.data.get('token', None),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class StarById(APIView):
    """
    Вьюшка для получения звезды по айди
    """
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def get(self, request):
        id = request.GET.get("id", "")
        try:
            stars_set = Stars.objects.get(id=id)
            serializer_class = StarSerializer(stars_set)
            json = serializer_class.data

            user = Users.objects.get(username=json['username'])
            avatar = Avatars.objects.get(username=user.username)
            video = Videos.objects.get(username=user.username)

            json['video'] = str(video.video_hi)
            json['avatar'] = str(avatar.image)
            return Response(json, status=status.HTTP_200_OK)
        except Stars.DoesNotExist:
            # logger.debug(msg="Star id={} not found".format(id), exc_info=True)
            json = {"exception": "Звезда с  id={} не была найдена".format(id)}
            return Response(json, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            # logger.warning(msg="Field 'id' expected a number but got {}.".format(id), exc_info=True)
            json = {"exception": "Поле 'id' ожидает чилсло, но было принято {}".format(id)}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class StarsList(APIView):
    """
    Получаем список всех звезд
    """
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        stars_list = Stars.objects.filter().values()

        for i in range(len(stars_list)):
            star_ex = Stars.objects.get(users_ptr_id=stars_list[i]['id'])
            tags = star_ex.tags.all().values()
            stars_list[i]['tags'] = tags

        return Response(stars_list, status=status.HTTP_200_OK)


class StarTagFilter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        filter = []
        for key, value in request.data.items():
            filter.append(key)
            filter.append(value)
        star_ex = Stars.objects.filter(tags__name__in=filter).values()
        return Response(star_ex, status=status.HTTP_200_OK)


class StarByCategory(APIView):
    """
    Вьюшка для получения спсика звезд по айди категории
    """
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        """
        1. Получаем QuerySet из таблицы звезд по id категории
        2. Переводим в дату и отдаем с 200 response
        :return:
        """
        id = request.GET.get("id", "")
        try:
            stars_set = Stars.objects.filter(cat_name_id=id)
            serializer_class = StarSerializer(stars_set, many=True)
            json = serializer_class.data

            avatar_set = Avatars.objects.all()
            serial_avatar = AvatarSerializer(avatar_set, many=True)
            avatar_data = serial_avatar.data
            for i in range(len(json)):
                set = Likes.objects.filter(star_id=json[i]['id']).count()
                json[i]['likes'] = set
                for j in range(len(avatar_data)):
                    if json[i]['username'] == avatar_data[j]['username']:
                        json[i]['avatar'] = avatar_data[j]['image']
                        video = Videos.objects.get(username=json[i]['username'])
                        json[i]['video'] = video.video_hi.url

            try:
                if json == []:
                    raise Stars.DoesNotExist
            except Stars.DoesNotExist:
                json = {"exception": "Не найдено звезд в категории id = {}".format(id)}
                return Response(json, status=status.HTTP_404_NOT_FOUND)
            return Response(json, status=status.HTTP_200_OK)
        except ValueError:
            json = {"exception": "Поле 'id' ожидает чилсло, но было принято '{}'".format(id)}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RateStar(APIView):
    """
    Вьюшка для обновления рейтинга звезды
    """
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def put(self, request, format='json'):
        """
        Получаем Request вида:
        {
            "rating": "5",
            "adresat": 1,
            "adresant": 3
        }, где
            :param rating: int - сама оценка
            :param adresat: int - id заказчика, который поставил оценку
            :param adresant: int - id звезды, которой поставили оценку
        1. Получаем QuerySet из таблицы Рейтинга по айди звезды
           Суммируем все оценки и получаем среднее с округлением в большую сторону
        2. Получаем QuerySet из таблицы Звезд по айди звезды
           Записываем новый рейтинг
        3. Response в зависимости от исхода
        :return: 201 - успещная запись
                 418 - не валидные данные
                 404 - не валидные id
        """
        res: int() = 0

        try:
            obj = Ratings.objects.get(adresant=request.data['adresant'], adresat=request.data['adresat'])
            return Response({'Рейтинг уже выставлен'}, status=status.HTTP_403_FORBIDDEN)
        except Ratings.DoesNotExist:
            serializer = RatingSerializer(data=request.data)

            if serializer.is_valid():
                rating = serializer.save()
                if rating:
                    # json = serializer.data
                    queryset = Ratings.objects.filter(adresant=request.data['adresant'])
                    serializtor = RatingSerializer(queryset, many=True)
                    json = serializtor.data

                    for i in range(len(json)):
                        res += json[i]['rating']
                    uprate = ceil(res / len(json))

                    starset = Stars.objects.get(users_ptr_id=request.data['adresant'])
                    starset.rating = str(uprate)
                    starset.save()
                    # serialstar = StarSerializer(data=starset, partial=True)
                    # if serialstar.is_valid():
                    return Response({"Оценка выставлена"}, status=status.HTTP_201_CREATED)

                    # return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    """
    Вьюшка для регистрации заказа и отправки уведомления на почту звезды
    """
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def post(self, request, format='json'):
        """
        Получаем request вида:
        {
            "customer_id": "1",
            "star_id": "5",
            "order_price": "15000.00",
            "for_whom": "Для Мамы",
            "comment": "Хочу поздравить маму с днем рождения",
            "status_order": "New"
            "by_date"
        }, где
            :param customer_id: - id заказчика
            :param star_id: - id звезды
            :param order_price: - цена заказа
            :param for_whom: - Для кого заказ
            :param comment: - комментарий к заказу
            :param status_order: - стасус заказа (0 - New, 1 - Accepted, 2 - Completed)
        1. Создаем запись в бд заказа
        2. Если данные валидные, то забираем QuerySet по id звезды.
        3. Сериализуем данные и выцыпляем данные: 'email', 'username', 'price'
        4. Отправляем письмо на почту звезде с уведомлением о заказе
        :return: Response 201, если все хорошо. Response 400, если данные не валидные
        """
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            if order:
                star_queryset = Stars.objects.filter(users_ptr_id=request.data['star_id'])
                star_serializer = StarSerializer(star_queryset, many=True)

                star = star_serializer.data
                star_email = star[0]['email']
                star_username = star[0]['username']
                star_price = star[0]['price']
                SUBJECT = 'EXPROME: Уведомление!'
                TEXT_MESASGE = 'Уважаемый {}, вам пришел заказ поздравления на сумму {}'.format(
                    star_username, star_price
                )
                send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [star_email])
                data = {
                    'order_id': order_serializer.data['id'],
                    'message': 'Заказ создан!',
                }
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            json = {
                'Неверные данные для создания заказа.'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_418_IM_A_TEAPOT)


class StarOrderAccepted(APIView):
    """
    Вьюшка принятия или отклонения заяки на заказ со стороны звезды
    """
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def post(self, request, format='json'):
        """
        {
            'order_id'
            'accept' accept/reject
        }
        :param request:
        :param format:
        :return:
        """
        order_set = Orders.objects.get(id=request.data['order_id'])
        customer = Customers.objects.get(users_ptr_id=order_set.customer_id)
        customer_email = customer.email
        customer_username = customer.username
        if request.data['accept'] == 'accept':
            order_set.payment_id = ''
            order_set.status_order = 1
            order_set.save()
            SUBJECT = 'EXPROME: Уведомление!'
            TEXT_MESASGE = 'Уважаемый {}, ваш заказ был принят. ' \
                           'Приходите в EXPROME, чтобы оплатить его.'.format(
                customer_username
            )
            data = {'Заказ принят'}
        elif request.data['accept'] == 'reject':
            order_set.payment_id = ''
            order_set.status_order = -1
            order_set.save()
            SUBJECT = 'EXPROME: Уведомление!'
            TEXT_MESASGE = 'Уважаемый {}, ваш заказ был отклонён.' \
                           'Приходите заказывать еще поздравления в EXPROME'.format(
                customer_username
            )
            data = {'Заказ отклонен'}
        else:
            return Response({'Не установлен статус заказа.'}, status=status.HTTP_400_BAD_REQUEST)
        send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [customer_email])
        return Response(data, status=status.HTTP_201_CREATED)


class OrderPay(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        order_id = request.GET.get("order_id", "")
        link = 'https://exprome.ru:8080/payments/?order_id={}'.format(order_id)
        return Response({'link': link}, status=status.HTTP_200_OK)


class OrderPayCapture(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        order_id = request.GET.get("order_id", "")
        link = config.url + 'payments/notifications/?order_id{}'.format(order_id)
        return Response({'link': link}, status=status.HTTP_200_OK)


class ListCategory(APIView):
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        cat_set = Categories.objects.all()
        cat_serial = CategorySerializer(cat_set, many=True)
        json = cat_serial.data
        for i in range(len(json)):
            cat = CatPhoto.objects.get(category=json[i]['cat_name'])
            json[i]['category_photo'] = str(cat.image)


        return Response(json, status=status.HTTP_200_OK)


class OrdersListView(APIView):
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def get(self, request, format='json'):
        """
        Получаем request вида:
        {
            "user_id": "1",
            "is_star": 0
        }, где
            :param user_id: - id пользователя
            :param is_star: - статус звезды (0,1)

        :return:
        """
        is_star = request.GET.get("is_star", "")
        user_id = request.GET.get("user_id", "")

        if is_star == 'true':
            star_set = Stars.objects.get(users_ptr_id=user_id)
            star = star_set.username
            prof = star_set.profession

            try:
                order_set = Orders.objects.filter(star_id_id=user_id)
                serial_orders = OrderSerializer(order_set, many=True)

                json = serial_orders.data

                for i in range(len(json)):
                    customer = order_set[i].customer_id_id
                    user_set = Users.objects.get(id=customer)
                    username = user_set.username
                    avatar = user_set.avatar
                    try:
                        ava = Avatars.objects.get(id=avatar)
                        avatar_user = str(ava.image.url)
                    except Avatars.DoesNotExist:
                        avatar_user = 'нет фото'
                    json[i]['profession'] = prof
                    json[i]['customer_username'] = username
                    json[i]['customer_avatar'] = avatar_user

                return Response(json, status=status.HTTP_200_OK)
            except IndexError:
                response = {
                    'Заказов нет'
                }
                return Response(response, status=status.HTTP_200_OK)

        if is_star == 'false':
            user_set = Customers.objects.get(users_ptr_id=user_id)
            username = user_set.username

            try:
                order_set = Orders.objects.filter(customer_id_id=user_id)
                serial_orders = OrderSerializer(order_set, many=True)

                json = serial_orders.data

                for i in range(len(json)):
                    set_star = Stars.objects.get(users_ptr_id=order_set[i].star_id_id)
                    star = set_star.username
                    avatar = set_star.avatar_id
                    try:
                        ava = Avatars.objects.get(id=avatar)
                        avatar_user = str(ava.image.url)
                    except Avatars.DoesNotExist:
                        avatar_user = 'нет фото'
                    cat_id = set_star.cat_name_id.cat_name
                    json[i]['username'] = username
                    json[i]['profession'] = set_star.profession
                    json[i]['star'] = star
                    json[i]['star_avatar'] = avatar_user
                    json[i]['cat_name'] = cat_id
                    try:
                        video = Congratulations.objects.get(order_id=order_set[i].id)
                        json[i]['video'] = str(video.video_con)
                    except Congratulations.DoesNotExist:
                        json[i]['video'] = 'Видео не готово'

                return Response(json, status=status.HTTP_200_OK)
            except IndexError:
                response = {
                    'Заказов нет'
                }
                return Response(response, status=status.HTTP_200_OK)

        if (is_star != 'true') and (is_star != 'false'):
            return Response("Были переданы неверные данные. Не установлена личность пользователя.",
                            status=status.HTTP_400_BAD_REQUEST)


class PersonalAccount(APIView):
    """
    Вьюшка личного кабинета
    """
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def get(self, request, format='json'):
        """
        Получаем request вида:
        {
            "user_id": "1",
            "is_star": 0
        }, где
            :param user_id: - id пользователя
            :param is_star: - статус звезды (0,1)

        :return:
        """
        is_star = request.GET.get("is_star", "")
        user_id = request.GET.get("user_id", "")

        if is_star == 'true':
            star_set = Stars.objects.get(users_ptr_id=user_id)
            star_cust = ProfileStarSerializer(star_set)
            json = star_cust.data

            try:
                ava = Avatars.objects.get(username=star_set.avatar)
                avatar = str(ava.image)
            except Avatars.DoesNotExist:
                avatar = 'Нет фото'

            json['avatar'] = avatar

            try:
                set = Likes.objects.filter(star_id=user_id).count()
                json['likes'] = set
            except IndexError:
                json['likes'] = 0

            return Response(json, status=status.HTTP_200_OK)

        if is_star == 'false':
            user_set = Customers.objects.get(id=user_id)
            serial_user = ProfileCustomerSerializer(user_set)
            json = serial_user.data

            return Response(json, status=status.HTTP_200_OK)

        if is_star != 'true' and is_star != 'false':
            return Response("Были переданы неверные данные. Не установлена личность пользователя.",
                            status=status.HTTP_400_BAD_REQUEST)

    @logger.catch()
    def put(self, request, format='json'):
        tag = put.personal_account(request.data)
        return Response(tag)


class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @logger.catch()
    def post(self, request, *args, **kwargs):

        file_serializer = AvatarSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideohiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @logger.catch()
    def post(self, request, *args, **kwargs):

        file_serializer = VideoSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CongratulationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @logger.catch()
    def post(self, request, *args, **kwargs):

        set = Congratulations.objects.filter(order_id=request.data['order_id']).count()
        if set == 1:
            return Response({'Вы уже загрузили видео'}, status=status.HTTP_200_OK)

        else:
            try:
                # file_obj = request.FILES
                # request.data['video_con'] = file_obj
                file_serializer = CongratulationSerializer(data=request.data)
            except:
                return Response({"Неудачная попытка, вот че пришло:":
                                     {
                                         'video_con': str(request.data['video_con']),
                                         'star_id': request.data['star_id'],
                                         'order_id': request.data['order_id']
                                      }
                                 }, status=status.HTTP_418_IM_A_TEAPOT)

            if file_serializer.is_valid():
                video = file_serializer.save()
                if video:
                    order = Orders.objects.get(id=request.data['order_id'])
                    cust_username = order.customer_id.username
                    cust_email = order.customer_id.email
                    star = Stars.objects.get(id=request.data['star_id'])
                    star_username = star.username
                    SUBJECT = 'EXPROME: Уведомление!'
                    TEXT_MESASGE = 'Уважаемый {}, Вам пришло видео поздравление '.format(
                        cust_username, star_username
                    )
                    send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [cust_email])
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'данные невалид':
                    {
                        'video_con': str(request.data['video_con']),
                        'star_id': request.data['star_id'],
                        'order_id': request.data['order_id']
                    }
                }, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    @logger.catch()
    def get(self, request, format='json'):
        order = Orders.objects.get(id=request.data['order_id'])
        star = Stars.objects.get(id=request.data['star_id'])
        try:
            video = Congratulations.objects.get(order_id=request.data['order_id'])
            json = {
                'star_username': str(star.username),
                'order_price': order.order_price,
                'video': str(video.video_con)
            }
            return Response(json, status=status.HTTP_200_OK)
        except Congratulations.DoesNotExist:
            json = {
                'star_username': str(star.username),
                'order_price': order.order_price
            }
            return Response(json, status=status.HTTP_200_OK)


# Message View
class MessageView(APIView):

    permission_classes = [IsAuthenticated]

    @logger.catch()
    def get(self, request, format='json'):
        from_user = request.GET.get("from_user", "")
        user_id = request.GET.get("user_id", "")
        chat_id = int(from_user) + int(user_id)
        try:
            msg = MessageChats.objects.filter(chat_id=chat_id).order_by('message_id').values()
            if not msg:
                raise MessageChats.DoesNotExist
            else:
                return Response(msg, status=status.HTTP_200_OK)
        except MessageChats.DoesNotExist:
            return Response({'сообщений нет'}, status=status.HTTP_404_NOT_FOUND)


    @logger.catch()
    def post(self, request, format='json'):
        chat_id = int(request.data['from_user']) + int(request.data['user_id'])
        try:
            msg_history = len(MessageChats.objects.filter(chat_id=chat_id))
            msg_id = msg_history + 1
            obj = MessageChats(chat_id=chat_id, from_user=request.data['from_user'],
                               message=request.data['message'], message_id=msg_id)
            obj.save()

            try:
                star = Stars.objects.get(users_ptr_id=request.data['user_id'])

                if star.is_star:
                    mail.notification_self_mail(star=star.id)
            except Stars.DoesNotExist:
                pass

            return Response({'Отправлено'}, status=status.HTTP_200_OK)
        except:
            return Response({'ошибка при отправке'}, status=status.HTTP_404_NOT_FOUND)


# Likes View
class LikesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        try:
            obj_like = Likes.objects.get(star_id=request.data['star_id'], cust_id=request.data['cust_id'])
            return Response({'Лайк уже стоит'}, status=status.HTTP_403_FORBIDDEN)
        except Likes.DoesNotExist:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Оценка выставлена"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register via Google
class PreGoogleView(APIView):
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        response = yandex.send_request()
        json = {'link': 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?'
                        'redirect_uri=https://exprome.ru/&'
                        'prompt=consent&'
                        'response_type=code&'
                        'client_id=506165388319-il6eo99u4u3akgr7ul32uaj9jsgvjq05.apps.googleusercontent.com&'
                        'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid&'
                        'access_type=offline&'
                        'flowName=GeneralOAuthFlow'}

        return Response(json, status=status.HTTP_200_OK)


class MidGoogleView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        code = request.GET.get("code", "")
        response = yandex.token(code)
        #
        # try:
        #     us = YandexUsers.objects.get(access_token=response['access_token'])
        #     response['new'] = 0
        # except VkUsers.DoesNotExist:
        #     response['new'] = 1

        return Response(response, status=status.HTTP_201_CREATED)


# Register via Yandex API
class PreYandexView(APIView):
    """
    Временная тестовая вьюшка
    """
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        response = yandex.send_request()
        json = {'link': response}
        return Response(json, status=status.HTTP_200_OK)


class MidYandexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        code = request.GET.get("code", "")
        response = yandex.token(code)
        #
        # try:
        #     us = YandexUsers.objects.get(access_token=response['access_token'])
        #     response['new'] = 0
        # except VkUsers.DoesNotExist:
        #     response['new'] = 1

        return Response(response, status=status.HTTP_201_CREATED)


class YandexRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, format='json'):
        response = yandex.ya_auth(request.data['access_token'])
        username = response['login']
        email = response['default_email']
        if response['birthday'] == None:
            date_of_birth = '2000-05-05'
        else:
            date_of_birth = response['birthday']
        # avatar = response['default_avatar_id']
        phone = request.data['phone']
        data = {
            'username': username,
            'phone': phone,
            'email': email,
            'date_of_birth': date_of_birth,
            'password': response['id'],
            'register': 'yandex'
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            new = Users.objects.get(username=username)
            new.register = 'yandex'
            # new.avatar = avatar
            new.save()

            yandex_data = YandexUsers.objects.create(id_yandex=response['id'],
                                                     access_token=request.data['access_token'],
                                                     refresh_token=request.data['refresh_token'],
                                                     expires_in=request.data['expires_in'])
            yandex_data.save()

            return Response(
                data={
                    'id': new.id,
                    'token': serializer.data.get('token', None),
                    'email': email,
                    'date_of_birth': date_of_birth,
                    'username': username,
                    'phone': phone,
                    'is_star': new.is_star
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Register via VK API
class PreVKView(APIView):

    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, request, format='json'):
        response = vk.send_request()
        json = {'link': response}
        return Response(json, status=status.HTTP_200_OK)

class MidVKView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        code = request.GET.get("code", "")
        response = vk.token(code)

        return Response(response, status=status.HTTP_201_CREATED)


class VKRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, format='json'):
        try:
            response = vk.vk_auth(request.data['access_token'])
        except KeyError:
            return Response({'access_token not found'}, status=status.HTTP_400_BAD_REQUEST)
        username = response['screen_name']
        f_name = response['first_name']
        l_name = response['last_name']
        # birth_day = response['bdate']
        birth_day = '2000-05-05'
        pword = response['id']
        # photo = response['photo_max_orig']
        phone = request.data['phone']
        email = request.data['email']
        data = {
            'username': username,
            'phone': phone,
            'email': email,
            'date_of_birth': birth_day,
            'password': pword,
            'register': 'vk',
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            new = Users.objects.get(username=username)
            new.register = 'vk'
            # new.avatar = photo
            new.first_name = f_name
            new.last_name = l_name
            new.save()

            vk_data = VkUsers.objects.create(id_vk=response['id'],
                                             access_token=request.data['access_token'],
                                             expires_in=request.data['expires_in'])
            vk_data.save()

            return Response(
                data={
                    'id': new.id,
                    'token': serializer.data.get('token', None),
                    'username': username,
                    'phone': phone,
                    'email': email,
                    'date_of_birth': birth_day,
                    'is_star': new.is_star
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Login via Yandex API

class YandexLogInView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializerOauth

    def post(self, request, format='format'):
        response = yandex.ya_auth(request.data['access_token'])

        data_log = {
                    "email": response['default_email'],
                    "password": response['id']
                }

        serializer = self.serializer_class(data=data_log)

        if serializer.is_valid():
            cust_set = Customers.objects.get(email=response['default_email'])
            json = {
                'id': cust_set.id,
                'username': cust_set.username,
                'phone': cust_set.phone,
                'is_star': cust_set.is_star,
                'email': cust_set.email,
                'avatar': cust_set.avatar,
                'token': cust_set.token
            }
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Login via VK API

class VKLogInView(APIView):
    """
    Вьюшка с методом POST, но она думает, то тут GET
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializerOauth

    def post(self, request, format='format'):
        try:
            response = vk.vk_auth(request.data['access_token'])
        except KeyError:
            return Response({'access_token not found'}, status=status.HTTP_400_BAD_REQUEST)

        data_log = {
                    "email": request.data['email'],
                    "password": response['id']
                }

        serializer = self.serializer_class(data=data_log)

        if serializer.is_valid():
            cust_set = Customers.objects.get(email=request.data['email'])
            json = {
                'id': cust_set.id,
                'username': cust_set.username,
                'phone': cust_set.phone,
                'is_star': cust_set.is_star,
                'email': cust_set.email,
                'avatar': cust_set.avatar,
                'token': cust_set.token
            }
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format='format'):
        access_token = request.GET.get("access_token", "")
        email = request.GET.get("email", "")
        try:
            response = vk.vk_auth(access_token)
        except KeyError:
            return Response({'access_token not found'}, status=status.HTTP_400_BAD_REQUEST)

        data_log = {
                    "email": email,
                    "password": response['id']
                }

        serializer = self.serializer_class(data=data_log)

        if serializer.is_valid():
            cust_set = Customers.objects.get(email=email)
            json = {
                'id': cust_set.id,
                'username': cust_set.username,
                'phone': cust_set.phone,
                'is_star': cust_set.is_star,
                'email': cust_set.email,
                'avatar': cust_set.avatar,
                'token': cust_set.token
            }
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# send request form for new start
class RequestView(APIView):
    permission_classes = [AllowAny]

    @logger.catch()
    def post(self, request, format='json'):
        set = RequestSerializer(data=request.data)
        if set.is_valid():
            form = set.save()
            return Response({'Ваша заявка отправлена успешно.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'были предоставлены неверные данные.'}, status=status.HTTP_400_BAD_REQUEST)



