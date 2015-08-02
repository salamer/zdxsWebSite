from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from data.models import Data,Category,DataComment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import Http404
from django.contrib.auth.decorators import login_required,permission_required

from .forms import DataForm,DataCommentForm

# Create your views here.

def hello(request):
    return HttpResponse('hello world') 

def index(request):
	return render(request,"data_index.html")

def category_search(request,category):
	try:
		category=Category.objects.get(category=category)
	except Category.DoesNotExist:
		raise Http404
	posts=category.data_set.all()[::-1]
	paginator=Paginator(posts,10)
	page=request.GET.get('page')
	try:
		cur_posts=paginator.page(page)
	except PageNotAnInteger:
		cur_posts=paginator.page(1)
	except EmptyPage:
		cur_posts=paginator.page(paginator.num_pages)
	return render(request,"data_list.html",{'post':cur_posts})

@login_required(login_url='/login')
@permission_required('data.can_write',login_url='/')
def write(request):
	if request.method=="POST":
		form=DataForm(request.POST)
		if form.is_valid() and request.user.is_authenticated():
			try:
				category=Category.objects.get(category=form.cleaned_data['category'])
			except Category.DoesNotExist:
				category=Category.objects.create(category=form.cleaned_data['category'])

			data=Data.objects.create(
				title=form.cleaned_data['title'],
				summury=form.cleaned_data['summury'],
				editor=request.user.username,
				data=form.cleaned_data['data'],
				data_category=category)
			return HttpResponseRedirect('/data/')
	else:
		form=DataForm()
	return render(request,'data_write.html',{"form":form})

def post(request,id):
	try:
		post=Data.objects.get(id=id)
	except Data.DoesNotExist:
		raise Http404
	if request.user.is_authenticated:
		comment=post.datacomment_set.all()[::-1]
	else:
		comment=[]
	if request.method=='POST':
		form=DataCommentForm(request.POST)
		if form.is_valid():
			if request.user.is_authenticated:
				editor=request.user.username
			else:
				editor='anonymous'
			datacomment=DataComment.objects.create(
				editor=editor,
				comment=form.cleaned_data['comment'],
				link=post)
			return HttpResponseRedirect('/data/post/%s' %id)
	else:
		form=DataCommentForm()
	return render(request,'data_post.html',{"form":form,"comment":comment,"post":post})

@login_required(login_url='/login')
@permission_required('data.can_write',login_url='/')
def edit(request,id):
	try:
		post=Data.objects.get(id=str(id))
	except Data.DoesNotExist:
		raise Http404
	if request.method=="GET" and request.user.username==post.editor:
		post_data={'title':post.title,'data':post.data,'summury':post.summury}

		form=DataForm(post_data)
		
		return render(request,"data_edit.html",{"form":form})
	
	if request.method=="POST":
		new_data={'title':request.POST['title'],'data':request.POST['data'],'summury':request.POST['summury'],"category":post.data_category,}
		form=DataForm(new_data)
		
		if form.is_valid():
			post.title=form.cleaned_data['title']
			post.data=form.cleaned_data['data']
			post.summury=form.cleaned_data['summury']
			post.save()
			return HttpResponseRedirect('/data')
		else:
			return HttpResponseRedirect('/')

	else:
		return HttpResponseRedirect('/blog')