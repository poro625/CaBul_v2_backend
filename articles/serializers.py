from rest_framework import serializers
from articles.models import Feed, Comment, TaggedFeed
from users.models import User
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)        #테그

class CommentListSerializer(serializers.ModelSerializer): # 게시글 댓글을 보기위한 Serializer
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields='__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields=('id', 'user', 'content', 'created_at',)
        
class FeedCommentSerializer(serializers.ModelSerializer): #댓글 작성
    user = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:

        model = Comment
        fields='__all__'
        
class ArticleDetailSerializer(serializers.ModelSerializer):
    Feed_comment = CommentSerializer(many=True)

    def get_user(self, obj):
        return obj.user.email
        
    class Meta:
        model = Feed
        fields='__all__'

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields='__all__'
        
class FeedSerializer(serializers.ModelSerializer): #게시글 시리얼라이즈
    user = serializers.SerializerMethodField()
    comments = CommentListSerializer(source = "comment_set", many=True) # 게시글관련 댓글 보기위한 Serializer 설정
    
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Feed
        fields = '__all__'


class FeedListSerializer(serializers.ModelSerializer):
    like_count= serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like.count()

    class Meta:
        model = Feed
        fields='__all__'

class TagSerializer(TaggitSerializer, serializers.ModelSerializer): #테그
    tags = TagListSerializerField()

    class Meta:
        model = TaggedFeed
        fields = '__all__'