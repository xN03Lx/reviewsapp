from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    name = "reviewsapp.movies"
    verbose_name = _("Movies")
