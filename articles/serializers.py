from rest_framework import serializers

from articles.models import Feed,Comment
from users.models import User


class ArticleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Feed
        fields='__all__'