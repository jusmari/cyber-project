from django.contrib import admin
from django.urls import include, path

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("app/", include("cyber_site.urls")),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
]
