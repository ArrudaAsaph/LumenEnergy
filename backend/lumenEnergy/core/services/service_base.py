from django.db import transaction
from core.exceptions import (
    RecursoNaoEncontradoException,
    DadosInvalidosException
)


class ServiceBase:
    """
    Classe base para Services de domínio.
    Define o fluxo padrão e fornece hooks sobrescrevíveis.
    """

    model = None
    domain = None
    entity = None

    # ========================
    # VALIDACOES INTERNAS
    # ========================
    @classmethod
    def _validate_config(cls):
        if cls.model is None:
            raise RuntimeError("ServiceBase exige o atributo 'model'")
        if cls.domain is None:
            raise RuntimeError("ServiceBase exige o atributo 'domain'")
        if cls.entity is None:
            raise RuntimeError("ServiceBase exige o atributo 'entity'")

    # ========================
    # HOOKS (SOBRESCREVÍVEIS)
    # ========================
    @classmethod
    def antes_criacao(cls, *, data):
        pass

    @classmethod
    def depois_criacao(cls, *, obj):
        pass

    @classmethod
    def antes_atualizacao(cls, *, obj, data):
        pass

    @classmethod
    def depois_atualizacao(cls, *, obj):
        pass

    # ========================
    # BUSCAR
    # ========================
    @classmethod
    def buscar_por_id(cls, *, id):
        cls._validate_config()

        try:
            return cls.model.objects.get(id=id)
        except cls.model.DoesNotExist:
            raise RecursoNaoEncontradoException(
                message=f"{cls.entity} não encontrado",
                context={
                    "domain": cls.domain,
                    "entity": cls.entity,
                    "action": "buscar",
                    "field": "id",
                    "value": id,
                }
            )

    # ========================
    # LISTAR
    # ========================
    @classmethod
    def listar(cls, *, filtros=None):
        cls._validate_config()

        queryset = cls.model.objects.all()

        if filtros:
            filtros_validos = {
                chave: valor
                for chave, valor in filtros.items()
                if valor not in ("", None)
            }

            if filtros_validos:
                queryset = queryset.filter(**filtros_validos)

        return queryset

    # ========================
    # CRIAR
    # ========================
    @classmethod
    @transaction.atomic
    def criar(cls, *, data):
        cls._validate_config()

        cls.antes_criacao(data=data)

        try:
            obj = cls.model.objects.create(**data)
        except TypeError as e:
            raise DadosInvalidosException(
                message="Dados inválidos para criação",
                context={
                    "domain": cls.domain,
                    "entity": cls.entity,
                    "action": "criar",
                    "error": str(e),
                }
            )

        cls.depois_criacao(obj=obj)
        return obj

    # ========================
    # ATUALIZAR
    # ========================
    @classmethod
    @transaction.atomic
    def atualizar(cls, *, id, data):
        cls._validate_config()

        obj = cls.buscar_por_id(id=id)

        cls.antes_atualizacao(obj=obj, data=data)

        for campo, valor in data.items():
            setattr(obj, campo, valor)

        obj.save()

        cls.depois_atualizacao(obj=obj)
        return obj

    # ========================
    # DELETAR (OPCIONAL)
    # ========================
    @classmethod
    @transaction.atomic
    def deletar(cls, *, id):
        cls._validate_config()

        obj = cls.buscar_por_id(id=id)
        obj.delete()
        return None


