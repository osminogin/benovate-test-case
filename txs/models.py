from django.db import models

from users.models import User


class Transaction(models.Model):
    """
    Transaction model.
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    processed_time = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User, related_name='recipients')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
