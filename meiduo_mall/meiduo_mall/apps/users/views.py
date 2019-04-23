import re
from django import http
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from .models import User

# Create your views here.
from django.urls import reverse
from django.views import View
from pymysql import DatabaseError


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
        username = request.POST.get('user_name')
        print(username)
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        allow = request.POST.get('allow')

        #判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            print(username,password, password2, mobile, allow)
            return http.HttpResponseForbidden('缺少参数')
        #判断用户名是否是５－２０个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5－２０个字符的用户名')
        #判断密码是否为８－２０个字符
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden("请输入８－２０位的密码")
        #判断二次密码
        if password2 != password:
            return http.HttpResponseForbidden("两次密码不一致")
        #判断手机号
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        #判断手机号是否已经在数据库存在
        if User.objects.filter(mobile = mobile).count() > 0:
            return http.HttpResponseBadRequest('手机号已存在')

        # 判断是否勾选用户协议，已经在前端验证，不用重复
        # if allow != 'on':
        #     return http.HttpResponseForbidden('请勾选用户协议')

        #判断注册是否成功　user为数据库存储
        try:
            #user = User.objects.create(username=username, password=password, mobile=mobile )
            #其中，User是指这个表，保存密码时没有加密所以用create_user()方法
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 实现状态保持

        #request.session['user_id'] = user.id  利用session封装
        login(request, user)

        # 响应注册结果
        return redirect(reverse('contents:index'))

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        #对应ajax请求返回json格式，所以用JsonResponse
        return http.JsonResponse({'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'count': count})

