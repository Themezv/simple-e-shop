from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView
from django.utils.decorators import method_decorator

from .models import ServiceTile
from blog.models import Article
from .forms import AboutForm, ContactForm, ServiceTileForm


def index(request):
    tiles = ServiceTile.objects.all()
    articles = Article.objects.all().order_by('-published')[:3]
    form = ServiceTileForm
    services = [tile.pages for tile in tiles]
    can_add = len(services) < 6 and (request.user.is_staff or request.is_superuser)

    return render(request, 'homepage/index.html', {'services': services, 'form': form, "articles": articles, 'canAdd': can_add})


@method_decorator(login_required(), name="dispatch")
class NewTileView(CreateView):
    model = ServiceTile
    form_class = ServiceTileForm
    success_url = '/'

    def form_invalid(self, form):
        return HttpResponse("Плитка со ссылкой на эту услугу уже создана <a href=\"/\">Вернуться на главую </a>")


@method_decorator(login_required(), name="dispatch")
class DeleteTileView(DeleteView):
    model = ServiceTile
    form_class = ServiceTileForm
    success_url = '/'

    def get_object(self, queryset=None):
        id_tile_to_delete = int(self.request.POST.get('id-to-delete'))
        tile = ServiceTile.objects.get(pages__pk=id_tile_to_delete)
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

