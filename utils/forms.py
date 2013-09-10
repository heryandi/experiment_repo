from django import forms

class BootstrapControl(object):
    def __init__(self, **options):
        super(BootstrapControl, self).__init__(**options)
        self.widget.attrs["class"] = "form-control"

class BootstrapCharField(BootstrapControl, forms.CharField):
    def __init__(self, **options):
        super(BootstrapCharField, self).__init__(**options)

class BootstrapTextField(BootstrapControl, forms.CharField):
    def __init__(self, **options):
        self.widget = forms.Textarea()
        super(BootstrapTextField, self).__init__(**options)

class SimpleSearchCharField(BootstrapCharField):
    def __init__(self, **options):
        super(SimpleSearchCharField, self).__init__(**options)
        self.widget.attrs["placeholder"] = "Search"

class ExperimentSimpleSearchForm(forms.Form):
    query = SimpleSearchCharField(max_length=255, label = "", required = False)
