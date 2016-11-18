from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Tiles
from django.contrib.flatpages.models import FlatPage
from .forms import AboutForm, ContactForm, TilesForm


@csrf_protect
def index(request):
    tiles = Tiles.objects.all()
    form = TilesForm
    return render(request, 'homepage/index.html', {'tiles': tiles, 'form': form,})


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
