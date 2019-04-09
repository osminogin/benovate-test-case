from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class INNValidator(RegexValidator):
    """
    Validate INN (just 12 digits).
    """
    regex = r'^\d{12}$'
    message = _('INN number consists only of 12 digits')
