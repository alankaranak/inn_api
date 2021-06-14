import uuid
from rest_framework.decorators import action
from rest_framework.response import Response
from company.models import Company, Person
from rest_framework import status, permissions, viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from django.core import management


class PersonViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,]
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
    @action(methods=['GET',], detail=False, url_path='scan')
    def checkout_person(self, request, *args, **kwargs):
        """Проверка наличия записи о человеке."""
        data = request.data
        response_data = {'result': ''}
        uid = uuid.UUID(data.get('uid', None))
        inn = data.get('inn', None)
        address = data.get('address', '')
        response_data['result'] = Person.checkout_data(uid, inn, address)
        return Response(response_data)


class CompanyViewSet(viewsets.ViewSet):
    file_param_config = openapi.Parameter('inn', in_=openapi.IN_BODY, description='.csv файл выгрузки', type=openapi.TYPE_FILE)
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'inn'

    @action(methods=['GET',], detail=True, url_path='nol')
    def get_number_of_licenses(self, request, inn=None, *args, **kwargs):
        """Получить количество лицензий."""
        company = self.get_object(inn)
        if company is None:
            return Response({'nol': f"Компания с ИНН {inn} не найдена"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'nol': company.nol}, status=status.HTTP_200_OK)

    def get_object(self, inn):
        """Получить объект Компании по инн."""
        try:
            return Company.objects.get(inn=inn)
        except Company.DoesNotExist:
            return None


class CsvViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    parser_classes = [MultiPartParser, ]
    lookup_field = 'file_name'

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Файл обработан успешно',
            ),
        }
    )
    @action(methods=['POST'], detail=False, url_path='upload')
    def upload_file(self, request, *args, **kwargs):
        """Загрузить .csv файл запросом."""
        up_file = request.FILES['file']
        file_path = open(settings.IMPORT_DIR / up_file.name, 'wb+')
        for chunk in up_file.chunks():
            file_path.write(chunk)
        file_path.close()

        management.call_command('parse', filename=up_file.name)
        return Response('Успешно', status.HTTP_200_OK)
