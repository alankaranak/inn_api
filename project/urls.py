from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="INN API",
      default_version='v1',
      description="Описание",
   ),
   public=True,
)

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/', include(('company.urls', 'company'))),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger')
]
