from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    PolymorphicProxySerializer,
    extend_schema,
)
from rest_framework import serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from api.dao import FakeData

from .paginators import PageNumberPagination


class LiteDemoSerializer1(serializers.Serializer):
    schema = serializers.CharField(read_only=True, default="lite")
    first_name = serializers.CharField()


class DefaultDemoSerializer1(serializers.Serializer):
    schema = serializers.CharField(read_only=True, default="default")
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class HardDemoSerializer1(serializers.Serializer):
    schema = serializers.CharField(read_only=True, default="hard")
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    debt = serializers.IntegerField()


proxy_serializer = PolymorphicProxySerializer(
    component_name="Demo",
    serializers=[DefaultDemoSerializer1, LiteDemoSerializer1, HardDemoSerializer1],
    resource_type_field_name="schema",
)
schemas = {
    "default": DefaultDemoSerializer1,
    "lite": LiteDemoSerializer1,
    "hard": HardDemoSerializer1,
}
schema_parameter = OpenApiParameter(
    "schema", OpenApiTypes.STR, OpenApiParameter.QUERY, enum=list(schemas)
)


class DemoApiViewSet(ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPagination
    response_schema: str = "default"
    queryset = FakeData()
    request: Request

    @extend_schema(responses={"200": proxy_serializer}, parameters=[schema_parameter])
    def list(self, request, *args, **kwargs):
        self.response_schema = self.request.query_params.get("schema", "default")
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        return (
            schemas.get(self.response_schema)
            or schemas.get("default")
            or super().get_serializer_class()
        )
