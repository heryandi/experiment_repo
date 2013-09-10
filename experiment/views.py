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

from .forms import *
from .models import *

class ExperimentHome(ExperimentSearch, ListView):
    model = Experiment
    context_object_name = "experiments"

    def get_queryset(self):
        if "query" in self.request.GET:
            q = self.request.GET["query"]
            return Experiment.simple_search(q)
        return Experiment.objects.all()

class ExperimentDetail(ExperimentSearch, DetailView):
    slug_url_kwarg = "experiment_id"
    slug_field = "id"
    model = Experiment
    context_object_name = "experiment"

class ExperimentCreate(ExperimentSearch, CreateView):
    form_class = ExperimentForm
    template_name = "experiment/experiment_create_form.html"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owners.add(self.request.user)
        return super(ExperimentCreate, self).form_valid(form)

class ExperimentUpdate(ExperimentSearch, UpdateView):
    slug_url_kwarg = "experiment_id"
    slug_field = "id"
    model = Experiment
    form_class = ExperimentForm
    template_name = "experiment/experiment_update_form.html"

    def get_form_kwargs(self):
        kwargs = super(ExperimentUpdate, self).get_form_kwargs()
        kwargs["tags"] = " ".join(tag.name for tag in self.object.tag_set.all())
        return kwargs
