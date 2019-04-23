from django.conf.urls import url

from user_app import views

urlpatterns = [
    # 用户模块
    url(r'^hello', views.hello, name='hello'),
    url(r'^get_icon', views.get_icon, name='get_icon'),
    url(r'^get_vcode', views.get_vcode, name='get_vcode'),
    url(r'^login', views.login, name='login'),
    url(r'^update_self_data', views.update_self_data, name='update_self_data'),

    # 表白模块
    url(r'^uploadFirst', views.uploadFirst, name='uploadFirst'),
    url(r'^uploadImg', views.uploadImg, name='uploadImg'),
    url(r'^get_self_issue', views.get_self_issue, name='get_self_issue'),
    url(r'^delete_self_issue', views.delete_self_issue, name='delete_self_issue'),
    url(r'^index', views.index, name='index'),

    # 评论模块
    url(r'^do_comment', views.do_comment, name='do_comment'),
    url(r'^get_comments', views.get_comments, name='get_comments'),

    # 收藏模块
    url(r'^add_collection', views.add_collection, name='add_collection'),
    url(r'^get_collections', views.get_collections, name='get_collections'),

    # 关注模块
    url(r'^care', views.care, name='care'),
    url(r'^get_care_confessions', views.get_care_confessions, name='get_care_confessions'),

    # 通知模块
    url(r'^get_notice', views.get_notice, name='get_notice'),
    url(r'^get_public_notice', views.get_public_notice, name='get_public_notice'),
    url(r'^changeMessageState', views.changeMessageState, name='changeMessageState'),

    # 失物招领模块
    url(r'^get_lost_and_found', views.get_lost_and_found, name='get_lost_and_found'),

    # 二手商城模块
    url(r'^get_mall', views.get_mall, name='get_mall'),

    # 二手商城模块
    url(r'^get_others', views.get_others, name='get_others'),

]