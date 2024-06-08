"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from myapp import views

schema_view = get_schema_view(
    openapi.Info(
        title="DemoAPI",
        default_version='v1',
        description="Demo API to interact with keras NN",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pabcabmar3@alum.us.es"),
        license=openapi.License(name="BSD License"),
    ),
    url=settings.BASE_URL, 
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('api/predict_digits', views.PredictDigitsAPIView.as_view(), name='predict_digits'),
    path('hello', views.HelloWorldView.as_view(), name='hello_world'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
