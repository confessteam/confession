from django.core.cache import cache
from django.http import HttpResponse

from user_app.constant import OK, VERIFY_CODE_FAIL, BAD_DATA
from user_app.logic import get_code, send_msg, render_json, check_vcode
from user_app.models import User
from user_app.verify_form import UserForm


def hello(request):
    return HttpResponse('hello world')


# 用户模块
def get_vcode(request):
    '''获取验证码'''
    phonenum = request.GET.get('phonenum')
    vcode = get_code(4)
    res = send_msg(phonenum, vcode)
    cache.set('Vcode-%s' % phonenum, vcode, timeout=3600)
    return render_json(None, OK)


def login(request):
    '''无需注册的登录，如果不存在则创建'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    print(phonenum,vcode)
    if check_vcode(phonenum, vcode):
        user = User.objects.get_or_create(phone=phonenum)
        return render_json('sucess', OK)
    else:
        data = {
            'message':'vcode verify failed',
        }
        return render_json(data, VERIFY_CODE_FAIL)


def update_self_data(request):
    '''修改个人资料'''
    uid = request.id
    form = UserForm(request.POST)
    if not form.is_valid():
        return render_json(form.errors, BAD_DATA)
    user = form.save(commit=False)
    user.id = uid
    user.save()
    return render_json('mes', OK)







