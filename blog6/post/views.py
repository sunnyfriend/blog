# coding: utf-8

from django.shortcuts import render, redirect
from django.core.cache import cache
# from redis import Redis

from post.models import Article, Comment
from post.helper import page_cache

@page_cache(10)
def home(request):
	num_list = []
	articles_list = Article.objects.all()
	perpage = 5
	page = int(request.GET.get('page',1))
	pagenum = len(articles_list)//perpage
	if len(articles_list)%perpage == 0:
		pass
	else:
		pagenum += 1
	for i in range(pagenum):
		num_list.append(i+1)
	if page == num_list[-1]:
		articles = articles_list[(page-1)*5:]
	else:
		articles = articles_list[(page-1)*5:(page-1)*5+5]
	return render(request, 'home.html', {'articles': articles,'num_list':num_list})

# def home(request):
#     articles = Article.objects.all()
#     return render(request, 'home.html', {'articles': articles})

@page_cache(30)
def article(request):
    aid = int(request.GET.get('aid', 1))
    article = Article.objects.get(id=aid)
    comments = Comment.objects.filter(aid=aid)
    return render(request, 'article.html', {'article': article, 'comments': comments})

#function: cache the  article between db and view
# def article(request):
#     aid = int(request.GET.get('aid', 1))
#     if cache.get(aid):
#     	article = cache.get(aid)
#     else:
#     	article = Article.objects.get(id=aid)
#     	cache.set(aid,article,timeout=None)
#     comments = Comment.objects.filter(aid=aid)
#     return render(request, 'article.html', {'article': article, 'comments': comments})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        return render(request, 'create.html')


def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article})


def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})
