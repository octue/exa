from django.urls import include, re_path


urlpatterns = [
    re_path(r"^services/", include("django_twined.urls")),
]
