from django import forms
from django.utils import timezone

from utils.forms import *
from .models import *

class ExperimentForm(forms.ModelForm):
    title = BootstrapCharField(max_length = 255, required = True)
    paper = forms.FileField(required = False)
    description = BootstrapTextField(max_length = 4096, required = True)
    instruction = BootstrapTextField(max_length = 2048, required = True)

    class Meta:
        model = Experiment
        fields = ["title", "paper", "description", "instruction",]

    def __init__(self, *args, **kwargs):
        tag_initial = "" if "tags" not in kwargs else kwargs.pop("tags")

        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields["tags"] = BootstrapCharField(max_length = 1024, required = False, initial = tag_initial)

    def save(self, commit = True):
        m = super(ExperimentForm, self).save(commit = False)
        m.created_date = timezone.now()
        m.save()

        tags = []
        tag_names = self.cleaned_data["tags"].split()
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name = tag_name)
            tags.append(tag)
        m.tag_set = tags
        return m
