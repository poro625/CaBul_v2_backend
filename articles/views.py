
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed, Comment
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer, FeedSerializer, FeedListSerializer, FeedCommentSerializer
from django.db.models.query_utils import Q
import cv2
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import sys
import io
from django.forms.models import model_to_dict
import random


def transform(img, net):

    data = img.read()
    #인코딩
    encoded_img = np.fromstring(data, dtype = np.uint8)
    #다시 디코딩
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    
    h, w, c = img.shape
    #500x500으로 크기조정
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))
    #모델: 명화로 바꾸는 부분
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
    
    #어떤 명화로 바꿀지
    net.setInput(blob)
    output = net.forward()
    #아웃풋 크기 조정
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE
    #크기에 맞게 자르고 type을 바꿔줌
    output = np.clip(output, 0, 255)
    output = output.astype('uint8')
    
    output = Image.fromarray(output)
    output_io = io.BytesIO()
    output.save(output_io, format="JPEG")
    return output_io


class ArticlesFeedView(APIView):
    
    def get(self, request):
        articles = Feed.objects.all()
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def post(self,request):
    #     user = request.user
    #     now = datetime.now()
    #     model_list = ['articles/composition_vii.t7', 'articles/candy.t7', 'articles/feathers.t7', 'articles/la_muse.t7', 'articles/masaic.t7', 'articles/starry_night.t7', 'articles/the_scream.t7', 'articles/the_wave.t7', 'articles/udnie.t7']
    #     random.shuffle(model_list)
    #     output_io = transform(request.data['original_image'], net=cv2.dnn.readNetFromTorch(model_list[0]))
        
    #     new_pic= InMemoryUploadedFile(output_io, 'ImageField',f"{user.nickname}:{now}",'JPEG', sys.getsizeof(output_io), None)
        
    #     create_feeds = Feed.objects.create(
    #         user=user,
    #         title=request.data["title"],
    #         content=request.data["content"],
    #         category=request.data["category"],
    #         original_image=new_pic,
    #         transfer_image=new_pic,
    #     )
        
    #     painting_dict = model_to_dict(create_feeds)
    #     painting_dict['original_image'] = painting_dict['original_image'].url
        
    #     return Response(painting_dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class FeedCommentView(APIView): #댓글 (작성)(성창남)

    def post(self, request, feed_id):
        serializer = FeedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, feed_id=feed_id)
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