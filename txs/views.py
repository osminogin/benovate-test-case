from django.db import transaction
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .forms import TransactionForm


class TransactionView(FormView):
    template_name = 'transaction.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction')
    success_message = _('Transaction was successful')

    def form_valid(self, form):
        """ Make a transaction. """
        transaction_sum = form.cleaned_data['sum']
        sender = form.cleaned_data['sender']
        recipients = form.cleaned_data['recipients']

        with transaction.atomic():
            sender.refresh_from_db()
            sender.balance -= transaction_sum
            sender.save()
            personal_sum = transaction_sum / recipients.count()
            for recipient in recipients:
                recipient.balance += personal_sum
                recipient.save()

        return super().form_valid(form)
