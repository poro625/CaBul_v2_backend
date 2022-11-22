from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticlesFeedView.as_view(), name ='feed_upload_view' ), # 게시글 업로드
    path('/<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ), # 게시글 수정, 삭제
]

