import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from backend.models import User





@pytest.mark.django_db
def test_category_get(api_client, category_factory):
    url = reverse('backend:categories')
    category_factory(_quantity=5)
    response = api_client.get(url)
    assert response.status_code == 200
    assert (response.data['count']) == 5

@pytest.mark.django_db
def test_shop_get(api_client, shop_factory):
    url = reverse('backend:shops1-list')
    shop_factory(_quantity=10)
    response = api_client.get(url)
    assert response.status_code == 200
    assert (response.data['count']) == 10


@pytest.mark.django_db
def test_user_create(api_client):
    some_user = {
        "first_name": "HJK",
        "last_name": "test",
        "email": "test@ya.ru",
        "password": "qwer1234A",
        "company": "Ixjvkj",
        "position": "Assesor",
        "type": "shop"
    }

    url = reverse("backend:user-register")
    resp = api_client.post(url, data=some_user)
    assert resp.status_code == HTTP_201_CREATED
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_confirm(api_client, user_factory, confirm_email_token_factory):
    user = user_factory()
    token = confirm_email_token_factory()
    user.confirm_email_tokens.add(token)
    url = reverse("backend:user-register-confirm")
    resp = api_client.post(url, data={"email": user.email, "token": "wrong_key"})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is False
    resp = api_client.post(url, data={"email": user.email, "token": token.key})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_login(api_client):
    mail = "test@ya.ru"
    password = "cxxcv123456"

    some_user = {
        "first_name": "dfg",
        "last_name": "cvbdf",
        "email": mail,
        "password": password,
        "company": "Yandex",
        "position": "Specialist",
        "type": "shop"
    }

    url = reverse("backend:user-register")
    resp = api_client.post(url, data=some_user)
    assert resp.json().get('Status') is True

    user = User.objects.get(email=mail)
    user.is_active = True
    user.save()

    url = reverse("backend:user-login")
    resp = api_client.post(url, data={"email": mail, "password": password})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_details(api_client, user_factory):
    url = reverse("backend:user-details")
    user = user_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    api_client.force_authenticate(user=user)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('email') == user.email
    api_client.post(url, data={
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@mail.com",
        "password": "1234fvfvfvf",
        "company": "Company122",
        "position": "Position123"
    })
    resp = api_client.get(url)
    assert resp.json().get('company') == "Company122"
    resp = api_client.post(url, data={"type": "shop"})
    resp = api_client.get(url)
    assert resp.json().get('type') == "shop"

@pytest.mark.django_db
def test_products(api_client, user_factory, shop_factory, order_factory,
                  product_info_factory, product_factory, category_factory):

    url = reverse("backend:shops")
    shop = shop_factory()
    customer = user_factory()
    category = category_factory()
    prod = product_factory(category=category)
    prod_info = product_info_factory(product=prod, shop=shop)
    api_client.force_authenticate(user=customer)
    resp = api_client.get(url, shop_id=shop.id, category_id=category.id)
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('results')[0].get('name') == shop.name

@pytest.mark.django_db
def test_partner_upload(api_client, user_factory, shop_factory, category_factory, product_info_factory, product_factory):
    price = 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'
    url = reverse("backend:partner-update")
    u = user_factory()
    api_client.force_authenticate(user=u)
    u.is_active = True
    u.type = 'shop'
    u.save()

    shop = shop_factory()
    category = category_factory()

    prod = product_factory(category=category)
    prod_info = product_info_factory(product=prod, shop=shop)

    resp = api_client.post(url, data={"url": price})

