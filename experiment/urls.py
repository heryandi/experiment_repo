from django.conf.urls import patterns, include, url
import views
import views_s3

urlpatterns = patterns("",
    url(r"^$", views.ExperimentHome.as_view(), name="home"),
    url(r"^create/$", views.ExperimentCreate.as_view(), name="create"),
    url(r"^(?P<experiment_id>\d+)/$", views.ExperimentDetail.as_view(), name="detail"),
    url(r"^(?P<experiment_id>\d+)/update/$", views.ExperimentUpdate.as_view(), name="update"),

    url(r"^(?P<experiment_id>\d+)/image/$", views.ExperimentDetail.as_view(), name="image-home"),
    url(r"^(?P<experiment_id>\d+)/image/upload/$", views_s3.index, name="image-upload"),
    url(r"^(?P<experiment_id>\d+)/image/upload/init_multipart/$", views_s3.init_multipart, name="image-upload-init"),
    url(r"^(?P<experiment_id>\d+)/image/upload/send_chunk/$", views_s3.send_chunk, name="image-upload-send"),
    url(r"^(?P<experiment_id>\d+)/image/upload/complete_file/$", views_s3.complete_file, name="image-upload-complete"),
    url(r"^(?P<experiment_id>\d+)/image/upload/report/$", views_s3.report, name="image-upload-report")
)
