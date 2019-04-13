from django.db import transaction
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .forms import TransactionForm
from .models import Transaction


class TransactionView(FormView):
    """
    Make transaction view.
    """
    template_name = 'transaction.html'
    form_class = TransactionForm
    success_url = reverse_lazy('transaction')
    success_message = _('Transaction was successful')

    def form_valid(self, form):
        """ Make a transaction. """
        total_amount = form.cleaned_data['amount']
        sender = form.cleaned_data['sender']
        recipients = form.cleaned_data['recipients']

        with transaction.atomic():
            sender.refresh_from_db()

            # Credit and deposit money to users
            sender.balance -= total_amount
            sender.save()
            personal_sum = total_amount / recipients.count()
            for recipient in recipients:
                recipient.balance += personal_sum
                recipient.save()

            # Saving transaction for history
            tx = Transaction.objects.create(sender=sender, amount=total_amount)
            tx.recipients.set(recipients)

        return super().form_valid(form)


class HistoryView(ListView):
    """
    Transactions history view.
    """
    queryset = Transaction.objects.order_by('-processed_time')
    template_name = 'history.html'
    context_object_name = 'transactions'
