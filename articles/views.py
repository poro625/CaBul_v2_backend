from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.db.models.query_utils import Q
from articles.models import Comment,Feed

from articles.serializers import FeedSerializer
from rest_framework import generics
from rest_framework import filters


# Create your views here.  

class ArticlesFeedView(APIView):

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ArticlesFeedDetailView(APIView):

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
