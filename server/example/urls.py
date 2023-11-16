from django.urls import include, re_path


urlpatterns = [
    re_path(r"^integrations/octue/", include("django_twined.urls")),
]
