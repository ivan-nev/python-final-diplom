import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from backend.models import User





@pytest.mark.django_db
def test_category_get(api_client, category_factory):
    url = reverse('backend:categories')
    category_factory(_quantity=4)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 4







