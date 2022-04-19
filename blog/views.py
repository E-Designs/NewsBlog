from django.contrib.auth.models import User
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.db.models import Q 
from .utility import Visability_State, taglines
from django.contrib.auth.decorators import login_required
from .filters import postFilter
import random
# Create your views here.

def post_about(request):
    return render(request, 'blog/post_about.html')
    
def post_list(request):
    num = random.randint(0, len(taglines) -1)
    tagline = taglines[num]
    if request.user.is_staff:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    else:
        posts = Post.objects.filter(Q(published_date__lte=timezone.now()), Q(visability= Visability_State.pending) | Q(visability= Visability_State.approved)).order_by('-published_date')

    search = postFilter(request.GET, queryset=posts)
    posts = search.qs
    context = {'posts': posts,  'post_sub': Post.subject_choices, 'search': search, 'tag': tagline,  }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(story = post).order_by('-create_date')
    context = {
        'post': post,
        'post_sub': Post.subject_choices,
        'comments': comments,
        'number_of_believers': post.number_of_believers(),
        'number_of_sceptics': post.number_of_sceptics(),
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if(form.is_valid):
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.visability = Visability_State.pending
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user or request.user.is_staff:
         if request.method == "POST":
             form = PostForm(request.POST, request.FILES , instance=post)
             
             if form.is_valid():
                 post =form.save(commit=False)
                 post.author = post.author
                 post.published_date = timezone.now()
                 post.visability = Visability_State.pending
                 post.save()
                 return redirect('post_detail', slug=post.slug)
         else:
            form = PostForm(instance=post)
            return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('post_list')

def post_report(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.visability= Visability_State.under_review
        post.save()
        return redirect('post_list')
    else:
        return render(request, 'blog/post_report.html')

@login_required
def post_approve(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_staff:
        if request.method == "POST":
            post.visability= Visability_State.approved
            post.save()
            return redirect('post_list')
        else:
            return render(request, 'blog/post_approve.html')
    else:
        return redirect('post_list')

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.add_to_class or request.user.is_staff:
        if request.method == "POST":
            post.visability= Visability_State.hidden
            post.save()
            return redirect('post_list')
        else:
            return render(request, 'blog/post_delete.html')
    else:
        return redirect('post_list')

@login_required
def post_show(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.visability= Visability_State.approved
        post.save()
        return redirect('post_list')
    else:
        return render(request, 'blog/post_show.html')

@login_required
def new_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if (form.is_valid):
            comment = form.save(commit=False)
            comment.comment_author = request.user
            comment.story = post
            comment.create_date = timezone.now()
            comment.save()
            return redirect('post_detail', slug=slug)

    form = CommentForm()
    return render(request, 'blog/new_comment.html', {'form': form})

@login_required
def post_believer(request, slug):
    post = get_object_or_404(Post, slug=slug)
    mesg = 'Thank you for voting.'
    #check to see if the user is already a believer
    if post.believer.filter(id=request.user.id).exists():
        mesg = 'You are already a believer.'
    else: #add user to the list
         post.believer.add(request.user)
    #checks to see if the user is in the nonbeliever list
    if post.sceptic.filter(id=request.user.id).exists():
        post.sceptic.remove(request.user) 

    context={
        'slug': post.slug,
        'mesg': mesg
    }

    return render(request, 'blog/post_vote.html', context)

@login_required
def post_sceptic(request, slug):
    post = get_object_or_404(Post, slug=slug)
    mesg= 'Thank you for voting.'

    if post.sceptic.filter(id=request.user.id).exists():
        mesg = 'You are already a sceptic.'
    else:
        post.sceptic.add(request.user)

    if post.believer.filter(id=request.user.id).exists():
        post.believer.remove(request.user)

    context={
        'slug': post.slug,
        'mesg': mesg
    }

    return render(request, 'blog/post_vote.html', context)