from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from faker import Faker
from rest_framework import serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from api.dao import FakeData, Item

from .paginators import PageNumberPagination


class LiteDemoSerializer3(serializers.Serializer):
    first_name = serializers.CharField()


class DefaultDemoSerializer3(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class HardDemoSerializer3(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    debt = serializers.IntegerField()


schemas = {
    "default": DefaultDemoSerializer3,
    "lite": LiteDemoSerializer3,
    "hard": HardDemoSerializer3,
}
schema_parameter = OpenApiParameter(
    "schema", OpenApiTypes.STR, OpenApiParameter.QUERY, enum=list(schemas)
)
schema_examples = [
    OpenApiExample(
        f"schema = {k}",
        response_only=True,
        value=serializer(Item(Faker("ru"))).data,
    )
    for k, serializer in schemas.items()
]


class DemoApiViewSet(ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPagination
    response_schema = "default"
    queryset = FakeData()
    request: Request

    @extend_schema(
        parameters=[schema_parameter],
        examples=schema_examples,
    )
    def list(self, request, *args, **kwargs):
        self.response_schema = self.request.query_params.get("schema", "default")
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        return (
            schemas.get(self.response_schema)
            or schemas.get("default")
            or super().get_serializer_class()
        )
