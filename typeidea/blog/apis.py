from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post,Category
from .serializers import PostSerializer, PostDetailSerializer,CategorySerializer


@api_view()
def post_list(request):
    posts = Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializer(posts, many=True)
    return Response(post_serializers.data)


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer


# ModelViewSet：增,删,改,查所有接口
# class PostViewSet(viewsets.ModelViewSet):
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
         list:
         返回所有项目信息

         create:
         创建项目

         retrieve:
         获取某个项目的详细信息

         update:
         更新项目

         destroy：
         删除项目

        names:
        获取所有项目的名称

         interfaces:
        获取指定项目的所有接口信息
        """

    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]  # 写入权限校验，可读写接口还需要前端增加CSRF_TOKEN的获取（Django文档CSRF中的ajax）

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer