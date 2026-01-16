import django_filters
from contas.models import Pessoa


class PessoaFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="usuario__username",
        lookup_expr="icontains"
    )

    email = django_filters.CharFilter(
        field_name="usuario__email",
        lookup_expr="icontains"
    )

    tipo_usuario = django_filters.CharFilter(
        field_name="usuario__tipo_usuario"
    )

    ativo = django_filters.BooleanFilter(
        field_name="usuario__ativo"
    )

    class Meta:
        model = Pessoa
        fields = [
            "username",
            "email",
            "tipo_usuario",
            "ativo",
        ]
