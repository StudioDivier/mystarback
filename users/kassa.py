from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.views.generic import View
import uuid
import logging

from yandex_checkout import Configuration, Payment

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from MyStar import config
from MyStar.config import ID_KASSA, SK_KASSA
from users.serializers import OrderSerializer
from users.models import Orders
from users import models
from loguru import logger

from django.conf import settings

# config by loguru
# config
logger.add("log/debug.json", level="DEBUG", format="{time} {level} {message}", serialize=True,
           rotation="1 MB", compression="zip")

Configuration.account_id = ID_KASSA
Configuration.secret_key = SK_KASSA


class YandexPayment(APIView):
    """
    Создание платежа
    """
    permission_classes = [AllowAny]

    @logger.catch()
    def get(self, type_id):
        """
        Принимаем payment_id [GET]
        Создаем платеж
        Меняем статус платежа
        Сохраняем
        :param request:
        :param format:
        :return:
        """
        order_id = self.request.GET.get('order_id')
        order = Orders.objects.get(id=order_id)
        # status = int(order.status_order)
        value = order.order_price

        payment = Payment.create({
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}".format(config.url)
            },
            "capture": "false",
            "description": "Заказ №{}".format(order_id),
            "metadata": {
                "order_id": "37"
            }
        }, uuid.uuid4())

        # get confirmation url
        confirmation_url = payment.confirmation.confirmation_url
        order.payment_id = payment.id
        order.status_order = 2
        order.save()

        return HttpResponseRedirect(confirmation_url)


class YandexNotification(APIView):
    """
    Обработка платежа
    """

    permission_classes = [AllowAny]

    @logger.catch()
    def mailing(self, order_id):
        order = Orders.objects.get(id=order_id)
        star_q = models.Stars.objects.get(id=order.star_id_id)
        cust_q = models.Customers.objects.get(id=order.customer_id_id)

        mailer = [star_q.username, cust_q.username]

        SUBJECT = 'EXPROME: Уведомление!'
        TEXT_MESASGE = 'Уважаемый, {}.' \
                       'Заказ №{}  на сумму {}. Для {} от звезды {}.'

        for user in mailer:
            TEXT_MESASGE.format(user, order.id, cust_q.username, star_q.username)
            send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [user])


    @logger.catch()
    def post(self, request):
        """
        Подтверждение платежа и смена статуса заказа
        :param request:
        :return:
        """
        order_id = request.GET.get("order_id", "")
        order = Orders.objects.get(id=order_id)
        payment_id = order.payment_id
        # payment_id = '26fd1b35-000f-5000-a000-14c3cdc3d6c1'
        Payment.capture(payment_id)

        order = Orders.objects.get(id=order_id)
        order.status_order = 2
        order.save()

        self.mailing(order_id=order_id)

        return Response(status=200)
