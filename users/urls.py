from django.urls import include, path, re_path
from rest_framework import routers
from .views import (
CustomerCreate, StarCreate, StarsList, StarById, RateStar, StarByCategory,  OrderView, PersonalAccount,
LoginAPIView, StarOrderAccepted, ListCategory, AvatarUploadView, VideohiView, CongratulationView, OrderDetailCustomerView,
PreYandexView, YandexRegisterView, MidYandexView, OrdersListView, YandexLogInView, LikesView, RequestView,
MessageView, PreVKView, MidVKView, VKRegisterView, VKLogInView, StarTagFilter, OrderPay, OrderPayCapture,
)
from .views import PreGoogleView, MidGoogleView

from MyStar import settings
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('', include(router.urls)),

    re_path(r'^login/?$', LoginAPIView.as_view(), name=None),
    re_path(r'^registration/?$', CustomerCreate.as_view(), name=None),

    # views with uploads files
    path('upload/avatar/', AvatarUploadView.as_view(), name=None),
    path('upload/video/hi/', VideohiView.as_view(), name=None),
    path('upload/congritulatoin/', CongratulationView.as_view(), name=None),

    # category list
    path('categories/', ListCategory.as_view(), name=None),

    # views star
    path('star/create/', StarCreate.as_view(), name=None),
    path('star/getlist/', StarsList.as_view(), name=None),
    path('star/id/', StarById.as_view(), name=None),
    path('star/category/', StarByCategory.as_view(), name=None),
    path('ratestar/', RateStar.as_view(), name=None),
    path('star/like/', LikesView.as_view(), name=None),
    path('star/filter/', StarTagFilter.as_view(), name=None),

    # views orders
    path('order/', OrderView.as_view(), name=None),
    path('order/list/', OrdersListView.as_view(), name=None),
    path('order/accept/', StarOrderAccepted.as_view(), name=None),
    path('order/cust/detail/', OrderDetailCustomerView.as_view(), name=None),
    path('order/pay/', OrderPay.as_view(), name=None),
    path('order/pay/capture/', OrderPayCapture.as_view(), name=None),

    path('personal/', PersonalAccount.as_view(), name=None),
    path('message/', MessageView.as_view(), name=None),

    # google register
    path('pre-google-oauth/', PreGoogleView.as_view(), name=None),
    path('mid-google/', MidGoogleView.as_view(), name=None),

    # yandex register
    path('pre-yandex-oauth/', PreYandexView.as_view(), name=None),
    path('mid-yandex/', MidYandexView.as_view(), name=None),
    path('yandex-oauth/', YandexRegisterView.as_view(), name=None),

    # yandex login
    path('yandex-login/', YandexLogInView.as_view(), name=None),

    # vk register
    path('pre-vk-oauth/', PreVKView.as_view(), name=None),
    path('mid-vk/', MidVKView.as_view(), name=None),
    path('vk-oauth/', VKRegisterView.as_view(), name=None),

    # vk login
    path('vk-login/', VKLogInView.as_view(), name=None),

    # send request firm for new star
    path('form-request/star/', RequestView.as_view(), name=None)
]

# router = routers.DefaultRouter()
# router.register(r'stars', StarsViewSet)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)