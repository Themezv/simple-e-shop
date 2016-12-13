from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse


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


class ArticleEditView(UpdateView):
	template_name = "blog/article_form.html"
	model = Article
	form_class = ArticleForm

	@method_decorator(login_required())
	def dispatch(self, request, *args, **kwargs):
		return super(ArticleEditView, self).dispatch(request, *args, **kwargs)


class ArticleDeleteView(DeleteView):
	template_name = "blog/article_form.html"
	model = Article
	form_class = ArticleForm
	
	@method_decorator(login_required())
	def dispatch(self, request, *args, **kwargs):
		return super(ArticleDeleteView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		category_slug = super(ArticleDeleteView, self).get_context_data()['article'].category.slug
		return reverse('article_list', args=[str(category_slug)])
