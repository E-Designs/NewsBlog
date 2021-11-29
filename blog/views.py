from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment 
from .forms import CommentForm, PostForm
from django.db.models import Q 
from .utility import Visability_State
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_about(request):
    return render(request, 'blog/post_about.html')
    
def post_list(request):
    
    if request.user.is_staff:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    else:
        posts = Post.objects.filter(Q(published_date__lte=timezone.now()), Q(visability= Visability_State.pending) | Q(visability= Visability_State.approved)).order_by('-published_date')
    
    context = {'posts': posts, 'post_cat': Post.catagory_choices, 'post_sub': Post.subject_Choices  }
    return render(request, 'blog/post_list.html', context)

def post_authors_posts(request, find_author):
    posts = Post.objects.filter(author=find_author).order_by('published_date')
    pic = posts[0].author.profile.image.url
    auth = posts[0].author
    context = {
        'posts': posts,
        'pic': pic,
        'auth': auth,
        'post_cat': Post.catagory_choices,
        'post_sub': Post.subject_Choices,
    }
    return render(request, 'blog/post_authors_posts.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if (form.is_valid):
                comment = form.save(commit=False)
                comment.comment_author = request.user
                comment.story = post
                comment.create_date = timezone.now()
                comment.save()

    comments = Comment.objects.filter(story = pk).order_by('create_date')
    form = CommentForm()
    context = {
        'post': post,
        'post_cat': Post.catagory_choices,
        'post_sub': Post.subject_Choices,
        'comments': comments,
        'form': form, 
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
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
         if request.method == "POST":
             form = PostForm(request.POST, request.FILES , instance=post)
             
             if form.is_valid():
                 post =form.save(commit=False)
                 post.author = request.user
                 post.published_date = timezone.now()
                 post.visability = Visability_State.pending
                 post.save()
                 return redirect('post_detail', pk=post.pk)
         else:
            form = PostForm(instance=post)
            return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('post_list')

def post_report(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.visability= Visability_State.under_review
        post.save()
        return redirect('post_list')
    else:
        return render(request, 'blog/post_report.html')

@login_required
def post_approve(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
def post_show(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.visability= Visability_State.approved
        post.save()
        return redirect('post_list')
    else:
        return render(request, 'blog/post_show.html')