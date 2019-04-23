import pdb

from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from user_app.constant import NEED_LOGIN
from user_app.logic import render_json
from user_app.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        need_login_path = ['/api/proxy/user/update_self_data', '/api/proxy/user/issue',
                           '/api/proxy/user/get_self_issue', '/api/proxy/user/delete_self_issue',
                           "/api/proxy/user/get_collections", "/api/proxy/user/get_care_confessions",
                           "/api/proxy/user/add_collection", '/api/proxy/user/uploadImg', '/api/proxy/user/do_comment',
                           '/api/proxy/user/care', '/api/proxy/user/get_notice', '/api/proxy/user/changeMessageState']
        if path in need_login_path:
            token = request.GET.get('token')
            uid = cache.get(token)
            if uid:
                user = User.objects.filter(pk=uid).first()
                request.user = user
            else:
                return render_json('need login', NEED_LOGIN)
        else:
            return
