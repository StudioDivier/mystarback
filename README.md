**My Star**

*End-points*

* http://192.168.1.131:8080/api/login/ - логин

response: 

    201

* http://192.168.1.131:8080/api/registration/ - регистрация пользователя

response: 

    201

* http://192.168.1.131:8080/api/categories/ - GET категории

response: 

    201

* http://192.168.1.131:8080/api/star/create/- регистрация звезды

response: 

    201

* http://192.168.1.131:8080/password_reset/ - Смена пароля

request:

    {
        "email": "niletto@star.com"
    }
    
response: 

    {
        "status": "OK"
    }
    
    Приходит на почту ссылка типа:
        http://127.0.0.1:8000/password_reset/confirm/?token=121258a800cd8c3a66e9a849f1d3dd601c077f4
        Которая ведет на форму смены паоля
        
* http://127.0.0.1:8000/password_reset/confirm/?token=121258a800cd8c3a66e9a849f1d3dd601c077f4

request:

    {
    "password": "admin1234",
    "token": "121258a800cd8c3a66e9a849f1d3dd601c077f4"
    }
    
response:

    {
        "status": "OK"
    }
        
* http://192.168.1.131:8080/api/star/getlist/ - список всех звезд

response: 

    201

* http://192.168.1.131:8080/api/star/id/?id=1 - [GET] звезду по id

request:

    {
        "star_id" : "3"
    }

response:

    {
        "username": "zemfira",
        "phone": 9787896546,
        "email": "zemfira@star.com",
        "price": "15000.00",
        "cat_name_id": 2,
        "rating": 2,
        "is_star": true
    }

* http://192.168.1.131:8080/api/star/category/?id=1 - [GET] звезд по id категории

response:

    [
        {
            "username": "niletto",
            "phone": 9787892356,
            "email": "niletto@star.com",
            "price": "15000.00",
            "cat_name_id": 1,
            "rating": 2,
            "is_star": true
        }
    ]
    
*http://192.168.1.131:8080/api/star/filter/ - [POST] получить список звезд по тегам

request:

    {
        "filter": "Дом-2"
    }
    
response:

    [
        {
            "id": 39,
            "last_login": null,
            "first_name": "",
            "last_name": "",
            "date_joined": "2020-10-21T06:41:01.731831Z",
            "username": "poor10",
            "phone": 9989991122,
            "email": "poor10@test.com",
            "password": "pbkdf2_sha256$216000$w6IYSb1ZRKYh$cAFU9w9CNMANfouy74VSyBFllAYSIC+URr7l+8m8LyU=",
            "avatar": "media/avatars/1.jpg",
            "is_star": true,
            "is_staff": false,
            "is_superuser": false,
            "is_active": true,
            "register": "True",
            "users_ptr_id": 39,
            "price": 45000.0,
            "cat_name_id_id": 2,
            "rating": 5,
            "days": "0",
            "video_hi": "/1.jpg"
        }
    ]

* http://192.168.1.131:8080/api/ratestar/ - [PUT] проголосовать за звезду

request:

    {
        "rating": "1",
        "adresat": 1,
        "adresant": 3
    }

response: 

    201


* http://192.168.1.131:8080/api/star/like/ - [POST] поставить лайк

requset:
    
    {
        "star_id": 39,
        "cust_id": 1
    }
    
response:

    если лайк уже стоит:
        {'Лайк уже стоит'},  403
    если лайк:
        {"Оценка выставлена"} 201
    если отпраить плохие данныеЖ
        error.data 400

* http://192.168.1.131:8080/api/order/ - [POST] сделать заказ

request:

    {
        "customer_id": "1",
        "star_id": "3",
        "order_price": "4000.00",
        "for_whom": "Для Мамы",
        "comment": "Хочу поздравить маму с днем рождения",
        "status_order": "0"
    }

response: 

    201


* http://192.168.1.131:8080/api/orderaccept/ - [POST] звезда принимает/отклоняет заказ

request:

    {
        "order_id" : "5",
        "accept": "accept"
    }

response: 

    201
    
* http://192.168.1.131:8080/api/order/cust/detail/ - [GET] заказчик получает информацию по заказу

request:

    {
        "order_id": "2",
        "star_id": "5"
    }
    
response(если звезда не прислала поздравление):

    {
        "star_username": "Окимирон",
        "order_price": 88888.0
    }
    
response(если звезда прислала поздравление):

    {
        "star_username": "Окимирон",
        "order_price": 88888.0,
        "video": "congratulation/5/ef01bd85-3509-4cd2-907b-545dd7c799b5.mp4"
    }

* http://192.168.1.131:8080/api/personal/ - лк для звезды и заказчика

request:

    {
        "user_id": "1",
        "is_star": 0
    }

response:

    [
        {
            "username": "myname",
            "phone": 9941622229,
            "email": "poor@test.com",
            "date_of_birth": "1999-08-05",
            "is_star": false
        },
        {
            "orders": [
                {
                    "customer_id": 1,
                    "star_id": 3,
                    "payment_id": "",
                    "order_price": "4000.00",
                    "ordering_time": "2020-09-23T06:34:49.397971Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": 0
                },
                {
                    "customer_id": 1,
                    "star_id": 3,
                    "payment_id": "28153142-0a0c-47cd-b253-01e337034a69",
                    "order_price": "4000.00",
                    "ordering_time": "2020-09-22T13:45:05.643858Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": 1
                },
                {
                    "customer_id": 1,
                    "star_id": 2,
                    "payment_id": "",
                    "order_price": "15000.00",
                    "ordering_time": "2020-09-22T13:22:17.143066Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": -1
                }
            ]
        }
    ]


# Платежка
## Создать платеж
* http://192.168.1.131:8080/api/order/pay/?order_id=56 - создание платежа (холд)


    {
        "link": "http://192.168.1.131:8080/payments/?order_id=56"
    }

## Списание денег
* http://192.168.1.131:8080/api/order/pay/capture/?order_id=56 -  списание денег
   
   
   {
        "link": "http://192.168.1.131:8080/payments/notifications/?order_id56"
   }

# Загрузки файлов
* http://192.168.1.131:8080/api/upload/avatar/ - загрузить фотку (до 15 мб)

request(multipart/formdata):
response:
    ![](readme/upload%20avatar.png)

* http://192.168.1.131:8080/api/upload/video/hi/ - загрузить видео приветсвие звезды

request(multipart/formdata):
response:
    ![](readme/videohi.png)
    
* http://192.168.1.131:8080/api/upload/congritulatoin/ - загрузить поздравление

request(multipart/formdata):
response:
    ![](readme/cong.png)


# Messages
## Отправка сообщения
* http://192.168.1.131:8080/api/message/ -[POST] -запрос

request:
    
    {
        "from_user": 4,
        "user_id": 37,
        "message": "hi!"
    }
    
response:

    [
        "Отправлено"
    ] 
    200 OK
    
    
    [
        "ошибка при отправке"
    ] 
    404 OK

## Получить список сообщений
* http://192.168.1.131:8080/api/message/?user_id=<id>&from_user=<id>

response:

    [
        {
            "id": 16,
            "chat_id": 41,
            "from_user": 37,
            "message_id": 1,
            "message": "hi"
        },
        {
            "id": 17,
            "chat_id": 41,
            "from_user": 4,
            "message_id": 2,
            "message": "wru want?"
        },
        {
            "id": 18,
            "chat_id": 41,
            "from_user": 37,
            "message_id": 3,
            "message": "nthk"
        },
        {
            "id": 19,
            "chat_id": 41,
            "from_user": 4,
            "message_id": 4,
            "message": "well"
        }
    ]

# Yandex OAuth
## Register
### 1st STEP
* http://192.168.1.131:8080/api/pre-yandex-oauth/

response:
    
    {
        "link": "https://oauth.yandex.ru/authorize?response_type=code&client_id=afd8fcd32b0b46f287e8d9671b29622c"
    }
    
    приходит ссылка по которой пользователь должен перейти и пройти авторизацию в яндексе
    идет редирект на 
        * http://192.168.1.131:8080/api/mid-yandex/?code=4454043 
        
        который отдает:
        
        response:
        
            {
                "access_token": "AgAAAABGbolrAAadV473b-IDm0Vll2dOLX_qlJ4",
                "expires_in": 31358807,
                "refresh_token": "1:X7VqP0qppNU4g3Hz:n4aer7Oj-VAiWgGLa2v7queoMfLIEhwwmzGqhqQC-bE6jobpsuSG:qDnvpdzSuOxe-L1Ryp9h2w",
                "token_type": "bearer"
            }
            
            сохранить в localeStorage: 
                access_token
                expires_in
                refresh_token
        
###2nd STEP
* http://192.168.1.131:8080/api/yandex-oauth/ - [POST] - запрос

request:

    {
        "access_token": "AgAAAABGbolrAAadV473b-IDm0Vll2dOLX_qlJ4",
        "expires_in": 31445978,
        "refresh_token": "1:-LkGm4lbjCn8YTC-:H14t5f5FmLrvZCZ2jUcrM1_kXNmt-hRrGqcrhB2kWJN39t_Wkdi-:_VuPZZzgDWo9aoki7ZWTnA"
    }
    
response:

    {
        "id": 37,
        "username": "mystar999",
        "phone": 0,
        "is_star": false,
        "email": "mystar999@yandex.ru",
        "avatar": "27503/4rPlOgcuh9aRm0UZIRLZMUzNb7k-1",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImV4cCI6MTYwODQ1NTkyMH0.5voe3hImK8EjnSmUTDs4cLUrM1vnKY2UowMTu2BJB9I"
    }
    
## LOGIN
* http://192.168.1.131:8080/api/yandex-login/ - [POST] запрос

request:

    {
        "access_token": "AgAAAABGbolrAAadV473b-IDm0Vll2dOLX_qlJ4",
        "expires_in": 31445978,
        "refresh_token": "1:-LkGm4lbjCn8YTC-:H14t5f5FmLrvZCZ2jUcrM1_kXNmt-hRrGqcrhB2kWJN39t_Wkdi-:_VuPZZzgDWo9aoki7ZWTnA"
    }
    
response:

    {
        "id": 37,
        "username": "mystar999",
        "phone": 0,
        "is_star": false,
        "email": "mystar999@yandex.ru",
        "avatar": "27503/4rPlOgcuh9aRm0UZIRLZMUzNb7k-1",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImV4cCI6MTYwODQ1NTkyMH0.5voe3hImK8EjnSmUTDs4cLUrM1vnKY2UowMTu2BJB9I"
    }