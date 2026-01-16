import django_filters
from contas.models import Usuario


class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    tipo_usuario = django_filters.CharFilter()
    ativo = django_filters.BooleanFilter()

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "tipo_usuario",
            "ativo",
        ]
