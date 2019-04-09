from decimal import Decimal

import pytest
from django.shortcuts import reverse


@pytest.fixture(scope='function')
def admin_user(django_user_model):
    """ Неадминский юзер. """
    return django_user_model.objects.get(pk=1)


@pytest.fixture(scope='function')
def example_user(django_user_model):
    """ Неадминский юзер. """
    return django_user_model.objects.exclude(pk=1).first()


def test_simple_transaction(client, admin_user, example_user):
    """ Test simplest transaction. """
    starting_sender_balance = admin_user.balance
    starting_recepient_balance = example_user.balance
    transaction_sum = 666
    response = client.post(
        reverse('transaction'),
        {
            'sender': admin_user.pk,
            'recipients': example_user.inn_number,
            'sum': transaction_sum,
        },
        follow=True
    )
    assert response.status_code == 200

    admin_user.refresh_from_db()
    example_user.refresh_from_db()
    assert admin_user.balance == starting_sender_balance - transaction_sum
    assert example_user.balance == starting_recepient_balance + transaction_sum


def test_complex_transaction(client, admin_user, example_user):
    """ Test complex transaction. """
    starting_sender_balance = admin_user.balance
    starting_some_recepient_balance = example_user.balance
    transaction_sum = 100
    response = client.post(
        reverse('transaction'),
        {
            'sender': admin_user.pk,
            'recipients': '111111111111,222222222222',
            'sum': transaction_sum,
        },
        follow=True
    )
    assert response.status_code == 200

    admin_user.refresh_from_db()
    example_user.refresh_from_db()
    assert admin_user.balance == starting_sender_balance - transaction_sum
    assert example_user.balance == \
        starting_some_recepient_balance + transaction_sum / Decimal(2)
