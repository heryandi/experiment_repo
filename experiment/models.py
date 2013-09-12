from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query import Q
from django.utils import timezone

class Experiment(models.Model):
    title = models.CharField(max_length = 255, blank = False)
    description = models.TextField(max_length = 4096, blank = False)
    instruction = models.TextField(max_length = 2048, blank = False)
    paper = models.FileField(upload_to = "paper/%Y/%m/%d", blank = True)
    created_date = models.DateTimeField()
    owners = models.ManyToManyField(User)

    class Meta:
        ordering = ["-created_date"]

    def get_absolute_url(self):
        return reverse("experiment:detail", args=[str(self.id)])

    @staticmethod
    def simple_search(query):
        return Experiment.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | 
                Q(instruction__icontains=query) | Q(tag__name__exact=query)).distinct()

class Tag(models.Model):
    name = models.CharField(max_length = 255, primary_key=True, blank = False)
    experiments = models.ManyToManyField(Experiment)

    @staticmethod
    def exist(name):
        try:
            Tag.objects.get(pk = name)
            return True
        except Tag.DoesNotExist:
            return False

class S3File(models.Model):
    experiment = models.OneToOneField(Experiment)
    url = models.CharField(max_length = 2048)
    key = models.CharField(max_length = 2048)
