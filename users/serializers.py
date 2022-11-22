from rest_framework import serializers
from users.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer


class customRegistrationSerializer(RegisterSerializer):  # dj-rest-auth 회원가입 시리얼라이저
    
    nickname = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['name'] = self.validated_data.get('name', '')

        return data