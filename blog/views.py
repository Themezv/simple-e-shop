from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import Article
from shop.models import Category

from .forms import ArticleForm
# Create your views here.

class CategoryListView(ListView):
	template_name = "blog/category_list.html"
	model = Category
	slug_field = 'slug'
	slug_url_kwarg = 'category_slug'
	context_object_name = 'categories'


	# Не работает
	paginate_by = 5
	#############

	def get_queryset(self):
		query = self.request.GET.get('q')
		queryset_list = super(CategoryListView, self).get_queryset()
		if query:
			return queryset_list.filter(Q(title__icontains=query)).distinct()
		else:
			return queryset_list
		

class ArticleListView(ListView):
	template_name = "blog/article_list.html"
	model = Article
	context_object_name = 'object_list'
	slug_field = 'slug'
	slug_url_kwarg = 'category_slug'


	paginate_by = 10

	def get_queryset(self):
		query = self.request.GET.get('q')
		queryset_list = super(ArticleListView, self).get_queryset().filter(category__slug=self.kwargs['category_slug'])
		user = self.request.user

		##################Search###################
		query = self.request.GET.get("q")

		if query:
			return queryset_list.filter(
						Q(title__icontains=query) |     
						Q(content__icontains=query)).distinct()
		else:
			return queryset_list


	def get_context_data(self, **kwargs):
		context = super(ArticleListView, self).get_context_data(**kwargs)

		another_categories = Category.objects.all().exclude(slug=self.kwargs['category_slug'])[:10]
		context['another_categories'] = another_categories
		context['category_url'] = self.kwargs['category_slug']
		return context


class ArticleCreateView(CreateView):
	template_name = "blog/article_form.html"
	model = Article
	form_class = ArticleForm

	@method_decorator(login_required())
	def dispatch(self, request, *args, **kwargs):
		return super(ArticleCreateView, self).dispatch(request, *args, **kwargs)


class ArticleDetail(DetailView):
	template_name = "blog/article_detail.html"
	model = Article
	context_object_name = 'instance'

	def dispatch(self, request, *args, **kwargs):
		return super(ArticleDetail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ArticleDetail, self).get_context_data(**kwargs)
		instance = context['object']
		recent_articles = Article.objects.active().order_by('-published').exclude(slug=instance.slug)[:5]
		context['recent_articles'] = recent_articles
		return context


def article_edit(request,category_slug, article_slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Article, slug=article_slug)
	form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
	print(request.POST)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# messages.success(request, "<a href='#'>Item</a> edited", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())	
	context = {
		'instance': instance,
		'form': form
	}
	return render(request, "blog/article_form.html", context)


def article_delete(request,category_slug, article_slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Article, slug=article_slug)
	instance.delete()
	# messages.success(request, "Successfuly deleted", extra_tags="html_safe")
	context = {
	}
	return redirect("article_categoried_list", category_slug=category_slug)
