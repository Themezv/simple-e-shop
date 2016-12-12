from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, Http404
from .models import Tiles
from django.contrib.flatpages.models import FlatPage
from .forms import AboutForm, ContactForm, TilesForm
from django.core.exceptions import ObjectDoesNotExist


@csrf_protect
def index(request):
    tiles = Tiles.objects.all()
    form = TilesForm

    return render(request, 'homepage/index.html', {'tiles': tiles, 'form': form, })


def new_tile(request):
    if request.method == 'POST':
        form = TilesForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
        else:
            return HttpResponse("Плитка со ссылкой на эту услугу уже создана <a href=\"/\">Вернуться на главую </a>")
    else:
        return Http404


def delete_tile(request):
    if request.method == 'POST':
        id_tile_to_delete = int(request.POST['id-to-delete'])
        tile = Tiles.objects.get(pk=id_tile_to_delete)
        tile.delete()
        return redirect('/')
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
