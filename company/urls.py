from django.urls import path
from django.urls.conf import include
from company.views import CompanyViewSet, CsvViewSet, PersonViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'persons', PersonViewSet, basename='persons')
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'exchange', CsvViewSet, basename='exchange')


urlpatterns = [
    path('', include(router.urls)),
]
