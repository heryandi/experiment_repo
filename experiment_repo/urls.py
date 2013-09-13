from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", RedirectView.as_view(url = reverse_lazy("experiment:home")), name = "repo-home"),
    url(r"^experiment/", include("experiment.urls", namespace = "experiment")),
    url(r"^users/", include("experiment_user.urls", namespace = "experiment_user")),
    url(r"^accounts/", include("allauth.urls")),

    # For admin
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
