from django.conf.urls import url

from user_app import views

urlpatterns = [
    url(r'^hello', views.hello, name='hello'),
    url(r'^get_vcode', views.get_vcode, name='get_vcode'),
    url(r'^login', views.login, name='login')
]