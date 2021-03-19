from django.urls import path
from .views import home_view,post_view_json,post_comment_create_and_list_view,like_unlike_post,PostDeleteView,PostUpdateView

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('Liked/',like_unlike_post,name='like-post-view'),
    path('posts-json/', post_view_json, name='posts-view-json'),
    path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),

]
