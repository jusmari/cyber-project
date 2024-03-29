from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="missions/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("missions/", views.IndexView.as_view(), name="index"),
    path(
        "logout/",
        LogoutView.as_view(template_name="missions/logout.html"),
        name="logout",
    ),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("missions/create/", views.create_mission, name="create_mission"),
]
