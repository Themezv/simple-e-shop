from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from .models import Tiles
from .forms import AboutForm, ContactForm, TilesForm
##############

# class 

##############


@csrf_protect
def index(request):
    tiles = Tiles.objects.all()
    form = TilesForm

    return render(request, 'homepage/index.html', {'tiles': tiles, 'form': form, })


@method_decorator(login_required(), name="dispatch")
class NewTileView(CreateView):
    model = Tiles
    form_class = TilesForm
    success_url = '/'

    def form_invalid(self, form):
        return HttpResponse("Плитка со ссылкой на эту услугу уже создана <a href=\"/\">Вернуться на главую </a>")


@method_decorator(login_required(), name="dispatch")
class DeleteTileView(DeleteView):
    model = Tiles
    form_class = TilesForm
    success_url = '/'

    def get_object(self):
        id_tile_to_delete = int(self.request.POST.get('id-to-delete'))
        tile = Tiles.objects.get(pk=id_tile_to_delete)
        return tile


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

