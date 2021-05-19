"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from .custom_site import custom_site
from config.views import LinkView
from comment.views import CommentView

from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from blog.apis import post_list, PostListAPIView, PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register('post', PostViewSet, basename='api-post')
router.register('category', CategoryViewSet, basename='api-category')

urlpatterns = [
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
    path('link/', LinkView.as_view(), name='link_list'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('', include('blog.urls')),
    path('rss/', LatestPostFeed(), name='rss'),
    path('sitemap.xml/', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap),
         {'sitemaps': {'posts': PostSiteMap}}),
    path('ckeditor', include('ckeditor_uploader.urls')),
    # path('api/post',post_list,name='post_list'),
    # path('api/post',PostListAPIView.as_view(),name='post_list'),
    # path('api/', include(router.urls)),
    # path('api/docs/', include_docs_urls(title='typeidea apis')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__', include(debug_toolbar.urls))]
