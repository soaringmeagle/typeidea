# function base view

# from django.http import HttpResponse
# from django.shortcuts import render
#
# from .models import Post, Category, Tag
# from config.models import SideBar
#
#
# # Create your views here.
#
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#     # if tag_id:
#     #     try:
#     #         tag = Tag.objects.get(id=tag_id)
#     #     except Tag.DoesNotExist:
#     #         post_list = []
#     #     else:
#     #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     # else:
#     #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#     #     if category_id:
#     #         try:
#     #             category = Category.objects.get(category_id)
#     #         except Category.DoesNotExist:
#     #             category = None
#     #         else:
#     #             post_list = post_list.filter(category_id=category_id)
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)
#     # return render(request, 'blog/list.html', context={'post_list': post_list})
#     # return HttpResponse('list page for Posts')
#
#
# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     # return render(request, 'blog/detail.html', context={'post': post})
#     return render(request, 'blog/detail.html', context=context)
#
#
# def post_edit(request, post_id):
#     return HttpResponse('post edit for post {post_id}.'.format(post_id=post_id))
#
#
# def post_delete(request, post_id):
#     return HttpResponse('post delete for post {post_id}.'.format(post_id=post_id))

# class base view
from datetime import date

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from config.models import SideBar
from .models import Post, Category, Tag
# from comment.models import Comment
# from comment.forms import CommentForm
from django.db.models import Q, F
from django.core.cache import cache


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(Category.get_navs())
        context.update({
            'sidebars': SideBar.get_all(),
        })
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, tag_id=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # 使用自定义comment_block标签，保持结构合理性（Post中不再处理Comment）
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_list': Comment.get_by_target(self.request.path),
    #         'comment_form': CommentForm(),
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 1分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24 * 60 * 60)  # 24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.kwargs.get('author_id')
        return queryset.filter(owner_id=owner_id)
