from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.db.models import Q 

# Create your views here.
def post_about(request):
    return render(request, 'blog/post_about.html')
    
def post_list(request):
    posts = Post.objects.filter(Q(published_date__lte=timezone.now()), Q(visability='p') | Q(visability='a')).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_authors_posts(request, find_author):
    posts = Post.objects.filter(author=find_author).order_by('published_date')
    pic = posts[0].author.profile.image.url
    auth = posts[0].author
    context = {
        'posts': posts,
        'pic': pic,
        'auth': auth
    }
    return render(request, 'blog/post_authors_posts.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if(form.is_valid):
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.visability = 'p'
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post =form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.visability = 'p'
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})