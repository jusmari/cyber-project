from django.db import models
from django.conf import settings
from django.forms import ModelForm


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Mission(models.Model):
    Country = models.ForeignKey(Country, on_delete=models.CASCADE)
    Spy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = ["Country", "description"]
        labels = {"Country": "Country", "description": "Description"}
        help_texts = {
            "Country": "Select a country",
            "description": "Enter a description",
        }
        error_messages = {
            "description": {"max_length": "This description is too long."}
        }
