from decimal import Decimal

import pytest
from django.shortcuts import reverse


@pytest.fixture(scope='function')
def admin_user(django_user_model):
    """ Админский юзер. """
    return django_user_model.objects.get(pk=1)


@pytest.fixture(scope='function')
def example_user(django_user_model):
    """ Неадминский юзер. """
    return django_user_model.objects.exclude(pk=1).first()


def test_send_money_page(client):
    """ Страница отправки шекелей. """
    response = client.get(reverse('transaction'))
    assert response.status_code == 200


def test_history_page(client):
    """ Страница истории транзакций. """
    response = client.get(reverse('history'))
    assert response.status_code == 200


def test_simple_transaction(client, admin_user, example_user):
    """ Test simplest transaction. """
    starting_sender_balance = admin_user.balance
    starting_recepient_balance = example_user.balance
    transaction_amount = 666
    response = client.post(
        reverse('transaction'),
        {
            'sender': admin_user.pk,
            'recipients': example_user.inn_number,
            'amount': transaction_amount,
        },
        follow=True
    )
    assert response.status_code == 200

    admin_user.refresh_from_db()
    example_user.refresh_from_db()
    assert admin_user.balance == starting_sender_balance - transaction_amount
    assert example_user.balance == starting_recepient_balance + transaction_amount


def test_complex_transaction(client, admin_user, example_user):
    """ Test complex transaction. """
    starting_sender_balance = admin_user.balance
    starting_some_recepient_balance = example_user.balance
    transaction_amount = 100
    response = client.post(
        reverse('transaction'),
        {
            'sender': admin_user.pk,
            'recipients': '111111111111,222222222222',
            'amount': transaction_amount,
        },
        follow=True
    )
    assert response.status_code == 200

    admin_user.refresh_from_db()
    example_user.refresh_from_db()
    assert admin_user.balance == starting_sender_balance - transaction_amount
    assert example_user.balance == \
        starting_some_recepient_balance + transaction_amount / Decimal(2)


def test_transaction_with_wrong_data(client, admin_user, example_user):
    """ Test transaction with wrong data. """
    response = client.post(
        reverse('transaction'),
        {
            'sender': admin_user.pk,
            'recipients': '111222333',  # Wrong data
            'amount': 'WRONG_DATA',
        },
        follow=True
    )
    assert response.status_code == 200  # No error code on form validation
    assert 'recipients' in response.context_data['form'].errors
    assert 'amount' in response.context_data['form'].errors
    assert b'form-control is-invalid' in response.content
