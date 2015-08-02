from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Blog,BlogComment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import Http404
from django.contrib.auth.decorators import login_required,permission_required

from .forms import BlogForm,CommentForm
# Create your views here.

def index(request):
	blog=Blog.objects.all()[::-1]
	paginator=Paginator(blog,10)
	page=request.GET.get('page')
	try:
		blog_article=paginator.page(page)
	except PageNotAnInteger:
		blog_article=paginator.page(1)
	except EmptyPage:
		blog_article=paginator.page(paginator.num_pages)
	return render(request,'blog_index.html',{'blogs':blog_article})

@login_required(login_url='/login')
@permission_required('blog.can_write',login_url='/')
def write(request):
	if request.method=="POST":
		form=BlogForm(request.POST)
		if form.is_valid() and request.user.is_authenticated():
			blog=Blog.objects.create(
				title=form.cleaned_data['title'],
				editor=request.user.username,
				body=form.cleaned_data['body'],
				summury=form.cleaned_data['summury'],)
			
			return HttpResponseRedirect('/blog')
	else:
		form=BlogForm()
	return render(request,'blog_write.html',{'form':form})

def post(request,id):
	try:
		post=Blog.objects.get(id=str(id))
		post.counts=+1
	    
		comment=post.blogcomment_set.all()[::-1]
	except Blog.DoesNotExist:
		raise Http404
	post.save()
	if request.method=='POST':
		form=CommentForm(request.POST)
		if form.is_valid() and request.user.is_authenticated():
			blogcomment=BlogComment.objects.create(
				commentator=request.user.username,
				comment=form.cleaned_data['comment'],
				link=post)
			return HttpResponseRedirect('/blog/post/%s' %id)
	else:
		form=CommentForm()
	return render(request,'blog_post.html',{'post':post,"comment":comment,"form":form})

@login_required(login_url='/login')
@permission_required('blog.can_write',login_url='/')
def edit(request,id):
	try:
		post=Blog.objects.get(id=str(id))
	except Blog.DoesNotExist:
		raise Http404
	if request.method=="GET" and request.user.username==post.editor:
		post_data={'title':post.title,'body':post.body,'summury':post.summury}

		form=BlogForm(post_data)
		
		return render(request,"blog_edit.html",{"form":form})
	else:
		return HttpResponseRedirect('/blog')
	if request.method=="POST":
		form=BlogForm(request.POST)
		if form.is_valid:
			post.title=form.cleaned_data['title']
			post.body=form.cleaned_data['body']
			post.summury=form.cleaned_data['summury']
			post.save()
			return HttpResponseRedirect('/blog')

	else:
		return HttpResponseRedirect('/blog')