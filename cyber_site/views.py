from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.db import connection

from cyber_site.models import Country, Mission, MissionForm


class IndexView(generic.ListView):
    model = Mission
    template_name = "missions/index.html"
    context_object_name = "data"

    def get_queryset(self):
        return {
            # FLAW 1: Authentication Bypass
            "missions": Mission.objects.all(),
            # FLAW 1: CORRECTION
            # "missions": Mission.objects.filter(Spy=self.request.user),
            "form": MissionForm(),
        }


class DetailView(generic.DetailView):
    model = Mission
    template_name = "missions/detail.html"


def create_mission(request):
    if request.method == "POST":
        form = MissionForm(request.POST)

        if form.is_valid():
            formData = form.cleaned_data
            print("AAAA", formData)

            country = formData["Country"]
            description = formData["description"]
            user = request.user

            # FLAW 2: SQL Injection
            # injected mission", 2, 2) --
            with connection.cursor() as cursor:
                cursor.execute(
                    f'INSERT INTO cyber_site_mission (description, Country_id, Spy_id) VALUES ("{description}",{country.id}, {user.id})',
                )

            # FLAW 2: CORRECTION
            # mission = Mission(Country=country, Spy=user, description=description)
            # mission.save()

            return redirect("index")

    else:
        form = MissionForm()

    return render(request, "name.html", {"form": form})
