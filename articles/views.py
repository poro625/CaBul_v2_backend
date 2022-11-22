from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed, Comment


class ArticlesMovieLikeView(APIView): # 좋아요
    def post(self, request,movie_id ):
        article = get_object_or_404(Feed, id=movie_id)
        if request.user in article.movie_like.all():
            article.movie_like.remove(request.user)
            return Response("좋아요취소했습니다", status=status.HTTP_200_OK)
        else:
            article.movie_like.add(request.user)
            return Response("좋아요했습니다", status=status.HTTP_200_OK)