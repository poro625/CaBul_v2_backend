from django.urls import path
from articles import views


urlpatterns = [

    path('<int:feed_id>/like/', views.ArticlesFeedLikeView.as_view(), name = 'feed_like_view'), #좋아요
    path('search/', views.ArticlesSearchView.as_view(), name = 'articles_search_view'), #검색
]

