from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework.viewsets import GenericViewSet

from api.dao import FakeData

from .paginators import PageNumberPagination


class LiteDemoSerializer2(serializers.Serializer):
    first_name = serializers.CharField()


class DefaultDemoSerializer2(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class HardDemoSerializer2(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    debt = serializers.IntegerField()


schemas = {
    "default": DefaultDemoSerializer2,
    "lite": LiteDemoSerializer2,
    "hard": HardDemoSerializer2,
}
schema_parameter = OpenApiParameter(
    "schema", OpenApiTypes.STR, OpenApiParameter.QUERY, enum=list(schemas)
)


class SchemaVersioning(AcceptHeaderVersioning):
    default_version = "default"
    allowed_versions = list(schemas)
    version_param = "schema"


class DemoApiViewSet(ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPagination
    response_schema = "default"
    queryset = FakeData()
    versioning_class = SchemaVersioning
    request: Request

    @extend_schema(
        description="Схемы: [default](?version=default#/experiments/experiments_2_items_list), [lite](?version=lite#/experiments/experiments_2_items_list), [hard](?version=hard#/experiments/experiments_2_items_list)",
    )
    def list(self, request, *args, **kwargs):
        self.response_schema = self.request.version
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        return (
            schemas.get(self.response_schema)
            or schemas.get("default")
            or super().get_serializer_class()
        )
