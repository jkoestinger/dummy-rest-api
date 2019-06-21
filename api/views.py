from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, mixins, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.contrib.auth import get_user_model

from blog.models import Post, Comment
from api.serializers import UserBaseSerializer, PostBaseSerializer, CommentBaseSerializer

User = get_user_model()


class UserViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class PostViewSet(NestedViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  GenericViewSet):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostBaseSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(NestedViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     GenericViewSet):
    model = Comment
    queryset = Post.objects.all()
    serializer_class = CommentBaseSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['parent_lookup_post']
        serializer.save(author=self.request.user, post_id=post_id)


class UserSelfView(APIView):

    def get(self, request, format=None):
        serializer = UserBaseSerializer(request.user, context={'request': request})
        return Response(serializer.data)
