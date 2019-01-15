from django.conf.urls import url

from user_app import views

urlpatterns = [
    # 用户模块
    url(r'^hello', views.hello, name='hello'),
    url(r'^get_vcode', views.get_vcode, name='get_vcode'),
    url(r'^login', views.login, name='login'),
    url(r'^update_self_data', views.update_self_data, name='update_self_data'),

    # 表白模块
    url(r'^issue', views.issue, name='issue'),
    url(r'^get_self_issue', views.get_self_issue, name='get_self_issue'),
    url(r'^delete_self_issue', views.delete_self_issue, name='delete_self_issue'),
    url(r'^index', views.index, name='index'),

    # 评论模块
    url(r'^do_comment', views.do_comment, name='do_comment'),

]