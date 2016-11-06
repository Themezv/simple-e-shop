from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Page, MainSetting


@csrf_protect
def index(request): 
    return render(request, 'homepage/index.html', {})
