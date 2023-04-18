import pytest
from rest_framework.test import APIClient
from model_bakery import baker







@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('backend.Category', **kwargs)

    return factory







