from django.urls import path

from .views import PostsList, PostDetail, SearchPosts
from .views import ArticleCreate, ArticleUpdate, ArticleDelete
from .views import NewsCreate, NewsUpdate, NewsDelete
from .views import upgrade_me, CategoryListView, subscribe

urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPosts.as_view(), name='search_posts'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/,<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/,<int:pk>/subscribe', subscribe, name='subscribe'),
]
