from decimal import Decimal

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.postgres.forms import SimpleArrayField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from users.models import User
from users.validators import INNValidator


class TransactionForm(forms.Form):
    """
    Transaction form.
    """
    sender = forms.ChoiceField()
    recipients = SimpleArrayField(
        forms.CharField(validators=[INNValidator])
    )
    sum = forms.DecimalField(decimal_places=2, max_digits=12)

    def clean_sender(self):
        """ Sender existence check. """
        sender_pk = self.cleaned_data.get('sender')
        try:
            sender = User.objects.get(pk=sender_pk)
        except ObjectDoesNotExist:
            raise ValidationError(_('Sender doesn\'t exists'))
        return sender

    def clean_recipients(self):
        """ Checks all recipients exists. """
        recipients_list = self.cleaned_data['recipients']
        recipients = User.objects.filter(inn_number__in=recipients_list)
        if len(recipients_list) != recipients.count():
            raise ValidationError(_('Some recipients doesn\'t exists'))
        return recipients

    def clean(self):
        super().clean()
        # Проверка баланса отправителя
        transaction_sum = Decimal(self.cleaned_data['sum'])
        if self.cleaned_data['sender'].balance < transaction_sum:
            raise ValidationError(
                _('Insufficient funds in the sender\'s account')
            )

        # Отправитель не входит в список получателей
        if self.cleaned_data['sender'] in self.cleaned_data['recipients']:
            raise ValidationError(_('You can\'t send money to yourself'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_balance_concat = Concat(
            'username', Value(' - '), 'balance', output_field=CharField()
        )
        # Выборка активных пользователей для выпадающего списка
        self.fields['sender'].choices = (
            User.objects.filter(is_active=True)
                .annotate(user_balance=user_balance_concat)
                .values_list('id', 'user_balance')
        )
