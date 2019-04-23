# from django import views
from django.conf.urls import url

from users import views
from users.views import RegisterView

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]