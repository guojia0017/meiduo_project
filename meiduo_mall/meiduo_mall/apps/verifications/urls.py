from django.conf.urls import url

from verifications import views


urlpatterns = [
    # 注册
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    url(r'^imagecheck/(?P<pic_code>.+)/(?P<uuid>.+)/$', views.CheckImageCode.as_view()),

]