from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns("",
    url(r"^$", views.ExperimentHome.as_view(), name="home"),
    url(r"^(?P<experiment_id>\d+)/$", views.ExperimentDetail.as_view(), name="detail"),
    url(r"^(?P<experiment_id>\d+)/update/$", views.ExperimentUpdate.as_view(), name="update"),
    url(r"^create/$", views.ExperimentCreate.as_view(), name="create"),
)
