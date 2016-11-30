from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect

from .models import Article
from shop.models import Category

from .forms import ArticleForm
# Create your views here.


def category_list(request):
	queryset_list = Category.objects.all()

	user = request.user

	##################Search###################

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(Q(name__icontains=query)).distinct()


	#################Paginator#################

	paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
	page_request_var='page' #url name 'page'=1,2,3,4...
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		'categories': queryset,#object_list v html
		'page_request_var': page_request_var, #v url num page
		'user': user,
	}

	return render(request, "blog/category_list.html", context)



def article_categoried_list(request, category_slug):
	queryset_list = Article.objects.filter(category__slug=category_slug).order_by('-updated')
	if not request.user.is_staff or not request.user.is_superuser:
		queryset_list = Article.objects.active().filter(category__slug=category_slug).order_by('-updated')

	user = request.user
	category_url = category_slug
	another_categories = Category.objects.all().exclude(slug=category_slug)[:10]

	##################Search###################

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query) |     
				Q(content__icontains=query)
				#Q(user__first_name__icontains=query) |
				#Q(user__last_name__icontains=query) 
				).distinct()


	#################Paginator#################

	paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
	page_request_var='page' #url name 'page'=1,2,3,4...
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		'object_list': queryset,#object_list v html
		'page_request_var': page_request_var, #v url num page
		'category_url':category_url,
		'another_categories':another_categories,
		'user': user,
	}

	return render(request, "blog/article_list.html", context)



def article_create(request, category_slug):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = ArticleForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		# instance.user = request.user 
		print(request.POST)
		instance.save()	
		# messages.success(request, "Successfuly created", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())	

	context = {
		'form': form
	}
	return render(request, "blog/article_form.html", context)



def article_detail(request, category_slug ,article_slug=None):
	instance = get_object_or_404(Article, slug=article_slug)
	recent_articles = Article.objects.active().order_by('-published').exclude(slug=instance.slug)[:5]#get first 5 obj
	user = request.user
	if instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	context = {
		'instance': instance,
		'recent_articles':recent_articles,
		'user': user,
	}
	return render(request, "blog/article_detail.html", context)



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
