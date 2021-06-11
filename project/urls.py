from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="INN API",
      default_version='v1',
      description="Описание",
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ]
)

urlpatterns = [
   path('', admin.site.urls),
   path('api/v1/', include(('company.urls', 'company'))),
   path('auth/token/', views.ObtainAuthToken.as_view(), name='get_token'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]
