from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles.models import Comment,Feed
from articles.serializers import FeedCommentSerializer

class FeedCommentView(APIView): #댓글 (작성)(성창남)

    def post(self, request,feed_id):
        serializer = FeedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,feed_id=feed_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FeedCommentDetailView(APIView):  #댓글(수정,삭제)(성창남)

    def put(self, request, feed_id, comment_id):

        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = FeedCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, feed_id, comment_id):
        comment = get_object_or_404(Comment, id= comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)        