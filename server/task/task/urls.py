"""
URL configuration for task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# from countries import views
from .views import LogoutView

# from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth import views as auth_views

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import home_view, CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Country API",
        default_version="v1",
        description="API for managing country data, including search, region, language, and admin controls.",
        terms_of_service="https://github.com/diptu/code-Fusion-AI/blob/main/LICENSE",
        contact=openapi.Contact(email="diptunazmulalam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("country/", include("countries.urls")),
    path("api/countries/", include("api.urls")),
    # Login
    path(
        "api/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="custom_token_obtain_pair",
    ),
    # path(
    #     "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    # ),  # login
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger docs URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
