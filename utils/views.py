from .forms import *

class ExperimentSearch(object):
    def get_context_data(self, **kwargs):
        context = super(ExperimentSearch, self).get_context_data(**kwargs)
        context["search_form"] = ExperimentSimpleSearchForm(self.request.GET)
        return context
