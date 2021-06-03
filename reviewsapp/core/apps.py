from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "reviewsapp.core"
    verbose_name = _("Core")
