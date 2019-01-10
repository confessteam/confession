import uuid

from django.core.cache import cache
from django.http import HttpResponse

from user_app.constant import OK, VERIFY_CODE_FAIL, BAD_DATA
from user_app.logic import get_code, send_msg, render_json, check_vcode, save_upload_file, save_issue_image
from user_app.models import User, Confess
from user_app.verify_form import UserForm


def hello(request):
    return HttpResponse('hello world')

# ===================# 用户模块================
def get_vcode(request):
    '''获取验证码'''
    phonenum = request.GET.get('phonenum')
    vcode = get_code(4)
    # res = send_msg(phonenum, vcode)
    cache.set('Vcode-%s' % phonenum, vcode, timeout=3600)
    print(cache.get('Vcode-%s' % phonenum))
    return render_json(None, OK)


def login(request):
    '''无需注册的登录，如果不存在则创建'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        user, _ = User.objects.get_or_create(phone=phonenum)
        token = uuid.uuid4().hex
        cache.set(token, user.id, timeout=3600)
        data = {
            'msg':"登录成功",
            'token':token
        }
        return render_json(data, OK)
    else:
        data = {
            'mesg':'登录失败',
        }
        return render_json(data, VERIFY_CODE_FAIL)


def update_self_data(request):
    '''修改个人资料'''
    uid = request.user.id

    # 处理上传图片
    icon = request.FILES.get('icon')
    filename = 'avatar-%s' % uid
    filepath, filename = save_upload_file(filename, icon, save_path='static/headIcon')

    # 处理个人文字信息保存
    exist_user = User.objects.get(pk=uid)
    form = UserForm(request.POST)
    if not form.is_valid():
        return render_json(form.errors, BAD_DATA)
    user = form.save(commit=False)
    user.id = uid # 保存用户id
    user.icon= filename # 用户头像文件名
    user.phone = exist_user.phone # 用户手机号
    user.save()
    return render_json(user.to_dict(), OK)


# ===================表白===============================
def issue(request):
    userID = request.user.id
    userName = request.user.u_name
    print(userName, userID)
    context = request.POST.get('context', None)
    image1 = request.FILES.get('image1', None)
    image2 = request.FILES.get('image2', None)
    image3 = request.FILES.get('image3', None)

    confess = Confess()
    confess.userID = userID
    confess.userName = userName
    confess.context = context
    confess.image1, confess.image2, confess.image3 = save_issue_image(userID, image1, image2, image3)
    confess.save()

    data = {
        'userid':userID,
        'username':userName,
        'context':context,
        'image1':confess.image1,
        'image2':confess.image2,
        'image3':confess.image3,
        'state':'待审核'
    }
    return render_json(data, OK)








