from rest_framework import response
from rest_framework.response import Response
from company.models import Company, Person
from django.shortcuts import render
from rest_framework import views, authentication, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IndexView(views.APIView):
    inn_param_config = openapi.Parameter('inn', in_=openapi.IN_QUERY, description='ИНН', type=openapi.TYPE_STRING)
    uid_param_config = openapi.Parameter('uid', in_=openapi.IN_QUERY, description='Идентификатор', type=openapi.TYPE_STRING)
    address_param_config = openapi.Parameter('address', in_=openapi.IN_QUERY, description='Адрес', type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        operation_description="Проверка наличия записи по ИНН, УИД или адресу",
        manual_parameters=[
            inn_param_config,
            uid_param_config,
            address_param_config
        ],
        responses={
            200: openapi.Response(
                description='Ответ о наличии совпадений',
                examples={
                    'application/json':{
                        "result": "1/0",
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        data = request.data
        response_data = {'result': ''}
        uid = data.get('uid', None)
        inn = data.get('inn', None)
        address = data.get('address', '')
        response_data['result'] = self.checkout_data(uid, inn, address)
        return Response(response_data)

    def checkout_data(self, uid, inn, address):
        """Последовательная проверка существования записи."""
        if not Person.checkout_uid(uid):
            return 0
        if not Company.checkout_inn_address(inn, address):
            return 0
        return 1
