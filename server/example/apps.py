from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExampleAppConfig(AppConfig):
    """Example app showing orchestration of octue services using django-twined"""

    name = "example"
    verbose_name = _("Example App using Django Twined")

    def ready(self):
        # Import tasks and signals only once the app is ready, in order to register them
        from . import signals  # noqa:F401, nopylint: disable=unused-import, import-outside-toplevel
        from . import tasks  # noqa: F401, pylint: disable=unused-import, import-outside-toplevel
