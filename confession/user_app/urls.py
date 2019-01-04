from django.conf.urls import url

from user_app import views

urlpatterns = [
    url(r'^hello', views.hello, name='hello')
]