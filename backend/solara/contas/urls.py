from django.urls import path
from contas.views import *

app_name = "contas"

urlpatterns = [
    path("cadastro/", CadastroView.as_view(), name = "cadastro-usuarios"),
]
