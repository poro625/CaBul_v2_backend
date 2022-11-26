from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserRegistrationTest(APITestCase):
    def test_registration(self):  #회원가입 성공 테스트
        url = reverse("rest_register")   # url name
        user_data = {
                "email":"test@naver.com",
                "name":"name",
                "nickname":"junseok",
                "password1":"password123@",
                "password2":"password123@"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 201)
    
    def test_registration_email_valid(self):  #회원가입 실패 테스트 (유효하지 않은 email)
        url = reverse("rest_register")   # url name
        user_data = {
                "email":"test",
                "name":"name",
                "nickname":"junseok",
                "password1":"password123@",
                "password2":"password123@"
            }
        response = self.client.post(url, user_data)  
        self.assertEqual(response.status_code, 400)


    def test_registration_password_valid(self):  #회원가입 실패 테스트 (비밀번호 validate 통과 X )
        url = reverse("rest_register")   # url name
        user_data = {
                "email":"test@naver.com",
                "name":"name",
                "nickname":"junseok",
                "password1":"1234",
                "password2":"1234"
            }
        response = self.client.post(url, user_data)  
        self.assertEqual(response.status_code, 400)
    
    def test_registration_password(self):  #회원가입 실패 테스트 (비밀번호 확인 불일치 )
        url = reverse("rest_register")   # url name
        user_data = {
                "email":"test@naver.com",
                "name":"name",
                "nickname":"junseok",
                "password1":"passoword123@",
                "password2":"password1234@"
            }
        response = self.client.post(url, user_data)  
        self.assertEqual(response.status_code, 400)


class LoginUserTest(APITestCase): # 로그인 성공 테스트 
    def setUp(self):  # DB 셋업
        self.data = {'email': 'test@naver.com', 'password': 'password123@', 'is_active':'1'}
        self.user = User.objects.create_user('test@naver.com', 'password123@')
        
    def test_login_failed(self):   # 로그인 성공 테스트 
        response = self.client.post(reverse('rest_login'), self.data)
        self.assertEqual(response.status_code, 400)