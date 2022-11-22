from rest_framework import serializers
from articles.models import Feed, Comment
from users.models import User


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields='__all__'
        
class FeedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

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