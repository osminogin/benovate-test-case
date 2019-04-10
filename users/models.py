from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser

from .validators import INNValidator


class User(AbstractUser):
    """
    Custom user model.
    """
    inn_number = models.CharField(
        max_length=12, unique=True, validators=[INNValidator()]
    )
    # Никаких float, т.к. точность!
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
