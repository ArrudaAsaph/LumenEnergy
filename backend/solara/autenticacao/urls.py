from django.urls import path
from autenticacao.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]
