from django.urls import path
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserViewSet, PostViewSet, CommentViewSet, UserSelfView

router = SimpleRouter()

user_list = router.register('users', UserViewSet, base_name="user")
user_list.register('posts', PostViewSet, base_name='users-post', parents_query_lookups=['author'])

post_list = router.register('posts', PostViewSet, base_name="post")\
    .register('comments', CommentViewSet, base_name='posts-comment', parents_query_lookups=['post'])

urlpatterns = router.urls
urlpatterns.append(path('login/', TokenObtainPairView.as_view()))
urlpatterns.append(path('user/', UserSelfView.as_view()))
