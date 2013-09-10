from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns("",
    url(r"^$", views.ExperimentUserHome.as_view(), name="home"),
    url(r"^(?P<user_username>[^/]+)/$", views.ExperimentUserDetail.as_view(), name="detail"),
    url(r"^(?P<user_username>[^/]+)/update/$", views.ExperimentUserUpdate.as_view(), name="update"),
)
