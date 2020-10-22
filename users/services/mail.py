from django.core.mail import send_mail
from django.conf import settings

from ..models import Stars
from .database import get


def notification_self_mail(star):

    star_set = Stars.objects.get(users_ptr_id=star)

    username = star_set.username
    email = star_set.email

    SUBJECT = 'MySTAR: Уведомление!'
    TEXT_MESASGE = 'Уважаемый {}, Вам пришло личное сообщение от заказчика. ' \
                   'Чтобы ответить на него перейдите в приложение'.format(username)
    send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [email])

    return True