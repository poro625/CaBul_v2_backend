from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer


class ArticlesFeedLikeView(APIView): # Feed 좋아요
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request,feed_id ):
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.like.all():
            feed.like.remove(request.user)
            return Response("좋아요취소했습니다", status=status.HTTP_200_OK)
        else:
            feed.like.add(request.user)
            return Response("좋아요했습니다", status=status.HTTP_200_OK)

class ArticlesSearchView(generics.ListAPIView): #검색
    serializer_class = ArticleSerializer

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    search_fields = ["title","description"]