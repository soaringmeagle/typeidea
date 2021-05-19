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

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView

# from blog import views

# extra_post_urlpatterns = [
#     path('', views.post_list, name='post_list'),
#     path('tag/<int:tag_id>/', views.post_list, name='post_list_tag'),
#     path('category/<int:category_id>/', views.post_list, name='post_list_category'),
#     path('detail/<int:post_id>/', views.post_detail, name='post_detail'),
# ]

extra_post_urlpatterns = [
    path('', IndexView.as_view(), name='post_list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='post_list_tag'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='post_list_category'),
    path('author/<int:author_id>/', AuthorView.as_view(), name='post_list_author'),
    path('detail/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchView.as_view(), name='search_post'),

]
urlpatterns = [
    path('', include(extra_post_urlpatterns)),
]


