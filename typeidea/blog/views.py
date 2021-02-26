from django.http import HttpResponse
from django.shortcuts import render

from .models import Post, Category, Tag
from config.models import SideBar


# Create your views here.

def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.get(category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             post_list = post_list.filter(category_id=category_id)
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)
    # return render(request, 'blog/list.html', context={'post_list': post_list})
    # return HttpResponse('list page for Posts')


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    # return render(request, 'blog/detail.html', context={'post': post})
    return render(request, 'blog/detail.html', context=context)


def post_edit(request, post_id):
    return HttpResponse('post edit for post {post_id}.'.format(post_id=post_id))


def post_delete(request, post_id):
    return HttpResponse('post delete for post {post_id}.'.format(post_id=post_id))
