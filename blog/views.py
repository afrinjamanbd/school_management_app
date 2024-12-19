from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.shortcuts import render, get_object_or_404

# Create your views here.
def get_common_context(title=None):
    posts = Blog.objects.order_by('-id')
    main_post = Blog.objects.order_by('-id').filter(Main_post=True).first()
    recents = Blog.objects.filter(section='Recent').order_by('-id')[:3]
    trendings = Blog.objects.filter(section='Trending').order_by('-id')[:3]
    python = Blog.objects.filter(category_id=1, status=1)
    php = Blog.objects.filter(category_id=2, status=1)
    java = Blog.objects.filter(category_id=3, status=1)
    javascript = Blog.objects.filter(category_id=4, status=1)
    rubi = Blog.objects.filter(category_id=5, status=1)
    categories = Category.objects.all()
    
 
    return {
        'title': title,
        'posts': posts,
        'main_post': main_post,
        'recents': recents,
        'categories': categories,
        'trendings': trendings,
        'python': python,
        'php': php,
        'java': java,
        'javascript': javascript,
        'rubi': rubi,
    }

def index(request):
    posts = Blog.objects.order_by('-id')
    context = {
        'posts' : posts,
    }
    print(context)  # Debugging output
    return render(request, 'blog/index.html', context)


def blog_detail(request, slug):
    # posts = Blog.objects.order_by('-id')
    categories = Category.objects.all()
    post = get_object_or_404(Blog, blog_slug=slug)
    comments = Comment.objects.filter(blog_id = post.id).order_by('-date')

    context = {
        # 'posts': post,
        'categories': categories,
        'post': post,
        'comments': comments,
    }
    return render(request, "blog_detail.html", context)


def category(request, slug):
    cat = Category.objects.all()
    blog_cat = Category.objects.filter(slug=slug)
    context = {
        'cat': cat,
        'active_category': slug,
        'blog_cat': blog_cat
    }
    return render(request, 'category.html', context)

def contact(request):
    context = get_common_context(title="Contact - Dev Skill")
    return render(request, 'blog/contact.html', context)

def python(request):
    context = get_common_context(title="Python - Dev Skill")
    return render(request, 'blog/python.html', context)

def php(request):
    context = get_common_context(title="PHP - Dev Skill")
    return render(request, 'blog/php.html', context)

def java(request):
    context = get_common_context(title="Java - Dev Skill")
    return render(request, 'blog/java.html', context)

def javascript(request):
    context = get_common_context(title="javaScript - Dev Skill")
    return render(request, 'blog/javascript.html', context)

def rubi(request):
    context = get_common_context(title="Rubi - Dev Skill")
    return render(request, 'blog/rubi.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug = slug)
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        website = request.POST.get('InputWeb')
        comment = request.POST.get('InputComment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        Comment.objects.create(
            post = post,
            name = name,
            email = email,
            website = website,
            comment = comment,
            parent = parent_comment
        )
        return redirect('blog_detail', slug)
    return redirect('blog_detail')
