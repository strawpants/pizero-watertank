from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from settings.models import TankConfig, TankForm
from django.http import HttpResponseRedirect

@login_required()
def settings(request):
    # # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TankForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            TankConfig.objects.update_or_create(defaults=form.cleaned_data)
            # process the data in form.cleaned_data as required
            # redirect to the same settings page (but now with settings loaded):
            return HttpResponseRedirect(f"/settings/")

    # if a GET (or any other method) we'll create a blank form or load the entries
    else:
        settingsobj=TankConfig.objects.first()
        form = TankForm(instance=settingsobj)

    return render(request,"settings.html",context={"form":form})
