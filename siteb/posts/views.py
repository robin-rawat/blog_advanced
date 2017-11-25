from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from comments.models import Comment
from django.db.models import Q
from django.contrib import messages
from urllib.parse import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


# Create your views here.
def post_home(request):
	return render(request,"base.html", {})

def post_create(request):
	if request.user.is_authenticated():
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "successfully created")
			return HttpResponseRedirect(instance.get_absolute_url())
		
		context = {
			"form":form,
		}	
		return render(request,"post_form.html", context)
	else:
		messages.success(request, "<b>You must login to create any post</b>", extra_tags='html_safe')
		return HttpResponseRedirect(reverse('posts:list'))


def post_detail(request, pk=None):
	instance = get_object_or_404(Post, id=pk)
	share_string = quote_plus(instance.content)
	#Post.objects.get(id=instance.id)
	initial_data = {
		"content_type" : instance.get_content_type,
		"object_id" : instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type=form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() ==1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
				user=request.user,
				content_type=content_type,
				object_id=obj_id,
				content=content_data,
				parent=parent_obj
			)
		messages.success(request, "commment successfully posted")
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments
	context={
		"title":"Post Detail",
		"instance" : instance,
		"share_string" : share_string,
		"comments" : comments,
		"comment_form" : form,
	}
	return render(request,"post_detail.html", context)

def post_list(request): 
	queryset_list = Post.objects.all()#.order_by("-timestamp")
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query)).distinct()
	#here a new this pagination applied to list view
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"title":"List",
		"object_list":queryset
	}
	return render(request,"post_list.html", context)
	#return HttpResponse("<h1>list</h1>")
def post_update(request, pk=None):
	"""here we can take instance.auth name and check directly"""#sorted

	instance = get_object_or_404(Post, id=pk)
	if request.user == instance.user or request.user.is_superuser:
		form = PostForm(request.POST or None, request.FILES or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "<a href='#'>Item</a>Saved", extra_tags='html_safe')
			return HttpResponseRedirect(instance.get_absolute_url())

		context={
			"title":instance.title,
			"instance" : instance,
			"form":form,
		}
		return render(request,"post_form.html", context)
	else:
		messages.success(request, "<b>You are not the author of post</b>", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	


def post_delete(request,pk=None):
	
	instance = get_object_or_404(Post, id=pk)
	if request.user == instance.user or request.user.is_superuser:
		instance.delete()
		messages.success(request, "successfully deleted")
		return redirect("posts:list")
	else:
		messages.success(request, "<b>You are not the author of post</b>", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
