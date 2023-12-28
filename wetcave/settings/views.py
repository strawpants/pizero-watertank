from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from settings.models import TankConfig, TankForm, MQTTConfig,MQTTForm
from django.http import HttpResponseRedirect,Http404

@login_required()
def settings(request,formid=0):
    if formid == 0 :
        Form=TankForm
        ConfigModel=TankConfig
    elif formid == 1:
        Form=MQTTForm
        ConfigModel=MQTTConfig
    else:
       raise Http404

    # # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ConfigModel.objects.update_or_create(defaults=form.cleaned_data)
            # process the data in form.cleaned_data as required
            # redirect to the same settings page (but now with settings loaded):
            return HttpResponseRedirect(f"/settings/{formid}")

    # if a GET (or any other method) we'll create a blank form or load the entries
    else:
        settingsobj=ConfigModel.objects
        if settingsobj.count() == 0:
            settingsobj=ConfigModel()
        else:
            settingsobj=settingsobj.first()
        form = Form(instance=settingsobj)
    return render(request,"settings.html",context={"form":form})

