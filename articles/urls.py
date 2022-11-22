from django.urls import path
from articles import views

urlpatterns = [

    path('', views.ArticlesView, name ='articles_view' ),
    path('<int:movie_id>/like/', views.ArticlesFeedLikeView.as_view(), name = 'movie_like_view'), #좋아요
    path('search/', views.ArticlesSearchView.as_view(), name = 'articles_search_view'), #검색
]

