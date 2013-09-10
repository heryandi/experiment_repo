from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from utils.views import *

class ExperimentUserHome(ExperimentSearch, ListView):
    model = User
    context_object_name = "experiment_users"

class ExperimentUserDetail(ExperimentSearch, DetailView):
    slug_url_kwarg = "user_username"
    slug_field = "username"
    model = User
    context_object_name = "experiment_user"

class ExperimentUserUpdate(ExperimentSearch, UpdateView):
    slug_url_kwarg = "user_username"
    slug_field = "username"
    model = User
    context_object_name = "experiment_user"
