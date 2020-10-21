from rest_framework import status
from ...models import Users
from ...serializers import ProfileCustomerSerializer


def personal_account(r):
    user_set = Users.objects.get(id=r['id'])
    if 'first_name' in r:
        user_set.first_name = r['first_name']
    if 'last_name' in r:
        user_set.last_name = r['last_name']
    if 'username' in r:
        try:
            obj = Users.objects.get(username=r['username'])
            if obj.id != r['id']:
                name = obj.username
                json = {'данный никнейм {} уже существует'.format(name)}
                return json, status.HTTP_400_BAD_REQUEST
        except Users.DoesNotExist:
            user_set.username = r['username']
    if 'email' in r:
        try:
            obj = Users.objects.get(username=r['email'])
            if obj.id != r['id']:
                email = obj.email
                json = {'данный email {} уже существует'.format(email)}
                return json, status.HTTP_400_BAD_REQUEST
        except Users.DoesNotExist:
            user_set.email = r['email']
    user_set.save()
    return status.HTTP_201_CREATED
