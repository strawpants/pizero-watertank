#from django.shortcuts import render


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required()
def dashboard(request):
    return HttpResponse("This will be the wetcave dashboard")
