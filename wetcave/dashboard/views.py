#from django.shortcuts import render


from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("This will be the wetcave dashboard")
