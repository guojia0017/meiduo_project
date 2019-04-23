from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser, User
from django.shortcuts import render

# Create your views here.
from django.views import View


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')
    def post(self,request):


        pass


# class User(AbstractUser):
#     user = User.objects.create_user(username, email, password, **extra_fields)
#     user = authenticate(username=username, password=password, **kwargs)
#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'
