from django.urls import path
from contas.views import *

app_name = "contas"

urlpatterns = [
    path("usuarios/", UsuarioView.as_view(), name="usuario-criar"),
    path("usuarios/<int:id>", UsuarioDetalheView.as_view(), name="usuario-criar"),
    path("cadastro/", CadastroView.as_view(), name = "cadastro-usuarios"),
    path("pessoa/", PessoaView.as_view(),name = "detalhe-pessoa"),
]
