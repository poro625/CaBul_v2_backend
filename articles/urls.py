from django.urls import path
from articles import views

urlpatterns = [

    path('', views.ArticlesView, name ='articles_view' ),
    path('<int:feed_id>/comment/', views.FeedCommentView.as_view(), name = 'feed_comment_view'),
    path('<int:feed_id>/comment/<int:comment_id>/', views.FeedCommentDetailView.as_view(), name = 'feed_comment_detail_view'),  
]

