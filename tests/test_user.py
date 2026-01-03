import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_demo():
    user_model = get_user_model()
    user = user_model.objects.create()

    same_user = user_model.objects.get(pk=user.pk)

    assert same_user == user
