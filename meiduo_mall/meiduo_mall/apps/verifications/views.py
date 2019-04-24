import redis
from django import http
from django.shortcuts import render
from meiduo_mall.libs.captcha.captcha import captcha
# Create your views here.
from django.views import View
from django_redis import get_redis_connection


from verifications import constants


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码
        text, code,image = captcha.generate_captcha()
        print("sdfsdfs")
        # 保存图片验证码
        #因为要存到ｒｅｄｉｓ中，所以要在dev.py中配置缓存配置ｒｅｄｉｓ
        redis_conn = get_redis_connection('verify_code')
        #'verify_code'为在dev.py中配置caches中的那个键
        # redis_conn.set(uuid,code)
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_EXPIRES, text)

        # 响应图片验证码
        # content_type='imgae/jpg' 告诉浏览器(响应头)我返回给你的是个图片,否则的话会是一个二进制码
        #　通过content_type=来告诉响应头，返回的这段二进制数据是图片，默认Ｒｅｓｐｏｎｓｅ是一个字符串
        return http.HttpResponse(image, content_type='imgae/jpg')

class CheckImageCode(View):

    def get(self,request,pic_code,uuid):

        print(pic_code,uuid)

        redis_conn = redis.Redis()
        uvalue = redis_conn.get(uuid)

        print(uvalue)
        if uvalue != pic_code:
            return http.JsonResponse({'count': 1})
        # 'verify_code'为在dev.py中配置caches中的那个键
        # redis_conn.set(uuid,code)

        #验证pic_code是否等于验证码
        else:
            return http.JsonResponse({'count': 0})


