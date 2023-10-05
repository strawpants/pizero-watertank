

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
def dashboard(request):
    return render(request,"dashboard.html",context={"content":"<h1>Dashboard data views</h1>"})
