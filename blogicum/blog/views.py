from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from blog.models import Category, Post
from .constants import POSTS_LIMIT


def index(request):
    now = timezone.now()
    template = 'blog/index.html'
    posts = Post.objects.select_related('location', 'category').filter(
        category__is_published=True,
        is_published=True,
        pub_date__lte=now).order_by('title')[:POSTS_LIMIT]

    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    now = timezone.now()
    posts = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )
    template = 'blog/detail.html'
    context = {'post': posts}

    return render(request, template, context)


def category_posts(request, category_slug):
    now = timezone.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    template = 'blog/category.html'
    posts = category.posts.all().filter(pub_date__lte=now, is_published=True)
    context = {
        'category': category,
        'post_list': posts
    }

    return render(request, template, context)
