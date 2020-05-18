"""Defines URLs models for the project."""
from django.urls import path

from netwio.views import CommentCreate
from netwio.views import home
from netwio.views import PostView, PostCreate, PostUpdate, PostDelete

app_name = 'netwio'


urlpatterns = [
    # ex: /netwio/
    path('', home, name='home'),
    # ex: /netwio/admin
    path('<str:username>', home, name='user_posts'),
    # ex: /netwio/post/2/
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    # ex: /netwio/post/create/
    path('post/create/', PostCreate.as_view(), name='create_post'),
    # ex: /netwio/post/1/update/
    path('post/create/<int:pk>/update', PostUpdate.as_view(), name='update_post'),
    # ex: /netwio/post/5/delete/
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),
    # ex: /netwio/post/5/comment/
    path('post/<int:pk>/comment/', CommentCreate.as_view(), name='create_comment'),
]
