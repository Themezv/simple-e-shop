from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, Http404
from .models import Tiles
from django.contrib.flatpages.models import FlatPage
from .forms import AboutForm, ContactForm, TilesForm
from shop.models import Service
from django.core.exceptions import ObjectDoesNotExist


@csrf_protect
def index(request):
    tiles = Tiles.objects.all()
    form = TilesForm

    return render(request, 'homepage/index.html', {'tiles': tiles, 'form': form, })


def new_tile(request):
    if request.method == 'POST':
        """page_number = request.POST.get('pages')
        service = Service.objects.get(pk=page_number)
        try:
            Tiles.objects.get(pages=service)
        except ObjectDoesNotExist:
            Tiles.objects.create(pages=service)
            return HttpResponse("New tile was saved")
        else:
            return HttpResponse("Zanyato")
        """
        form = TilesForm(request.POST)
        if form.is_valid():
            tile = form.save(commit=True)
            return redirect('/')
        else:
            return HttpResponse("Плитка со ссылкой на эту услугу уже создана <a href=\"/\">Вернуться на главую </a>")
    else:
        return Http404


def about_edit(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(FlatPage, url='/about/')    
    form = AboutForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("about")

    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, "homepage/FlatPagesForm.html", context)


def contacts_edit(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(FlatPage, url='/contacts/')    
    form = ContactForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("contacts")

    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, "homepage/FlatPagesForm.html", context)
