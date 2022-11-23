from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed, Comment, TaggedFeed
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer, FeedSerializer, FeedListSerializer, FeedCommentSerializer, TagSerializer
from django.db.models.query_utils import Q
import torch
import cv2
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import sys
import io
from django.forms.models import model_to_dict
import random
from uuid import uuid4
import uuid



def upload_category(img, serializer):
    feed = Feed.objects.get(id=serializer['id'])
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        imgs = [(f'.{img}')] # batch of images
        results = model(imgs)
        category_name = results.pandas().xyxy[0]['name'][0]
        feed.category = category_name
        feed.save()
    except(IndexError):
        category_name = '카테고리 없음'
        feed.category = category_name
        feed.save()



def transform(img, net, serializer):
    feed = Feed.objects.get(id=serializer['id'])
    now = uuid.uuid4()
    
    data = cv2.imread((f'.{img}'))
    
    #인코딩
    encoded_img = np.fromstring(data, dtype = np.uint8)
    
    #다시 디코딩
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    
    h, w, c = data.shape
    #500x500으로 크기조정
    img = cv2.resize(data, dsize=(500, int(h / w * 500)))
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
    # output_io = io.BytesIO()
    transfer_image = f"transfer_feed_images/{feed.user.nickname}_{now}.jpg"
    output.save(f"./media/{transfer_image}", "JPEG")
    feed.transfer_image = transfer_image
    feed.save()

    # return output_io



class ArticlesFeedView(APIView):
    
    def get(self, request):
        articles = Feed.objects.all()
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        
        serializer = FeedSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            img = serializer.data["original_image"]
            upload_category(img, serializer.data)
            
            model_list = ['articles/sample/composition_vii.t7', 'articles/sample/candy.t7', 'articles/sample/feathers.t7', 'articles/sample/la_muse.t7', 'articles/sample/mosaic.t7', 'articles/sample/starry_night.t7', 'articles.sample/the_scream.t7', 'articles/sample/the_wave.t7', 'articles/sample/udnie.t7']
            random.shuffle(model_list)
            
            net = cv2.dnn.readNetFromTorch(model_list[0])
            
            transform(img, net, serializer.data)
            
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
        

class ArticlesFeedDetailView(APIView): #게시글 상세조회, 수정, 삭제
    
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
        

class ArticlesSearchView(generics.ListAPIView): #검색
    queryset = Feed.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    search_fields = ["title"]

class TagView(generics.ListAPIView): #테그
    queryset = TaggedFeed.objects.all()
    serializer_class = TagSerializer
    