from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from portal_aluno.views import home_view
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='SmartYDUQS API')


schema_view = get_schema_view(
   openapi.Info(
      title="SmartYDUQS API",
      default_version='v1',
      description="Test description",
      terms_of_service="",
      contact=openapi.Contact(email="vitorgsom@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path("", include('gerenciador.urls')),
   #  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   #  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include("dashboard.urls")),
    path("alunos/", include("portal_aluno.urls")),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
