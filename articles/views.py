from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed, Comment
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer, FeedSerializer, FeedListSerializer
from django.db.models.query_utils import Q


# Create your views here.  

class ArticlesFeedView(APIView):
    
    def get(self, request):
        articles = Feed.objects.all()
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ArticlesFeedDetailView(APIView):
    
    def get(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, feed_id):
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            serializer = FeedSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, feed_id):
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            feed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

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

class ArticlesSearchView(generics.ListAPIView): 
    queryset = Feed.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    search_fields = ["title"]
