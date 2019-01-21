import uuid
from urllib.parse import urljoin

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse

from confession.settings import MY_STATIC_FILES_URL
from user_app.constant import OK, VERIFY_CODE_FAIL, BAD_DATA, ISSUE_NOT_EXIST, ISSUE_NOT_ALLOWED, GET_ICON_IMAGE_FAIL
from user_app.logic import get_code, send_msg, render_json, check_vcode, save_upload_file, save_issue_image, \
    many_to_dict
from user_app.models import User, Confess, Comment
from user_app.verify_form import UserForm


def hello(request):
    return HttpResponse('hello world jenkins123789')


# ===================# 用户模块================
def get_icon(request):
    '''获取用户头像'''
    phonenum = request.GET.get('phonenum')
    try:
        user = User.objects.get(phone=phonenum)
        data = {
            "icon": urljoin(MY_STATIC_FILES_URL, 'headIcon/' + user.icon),
            "msg": "success"
        }
        return render_json(data, OK)
    except:
        data = {
            "icon": '',
            "msg": "用户名或密码错误"
        }
        return render_json(data, GET_ICON_IMAGE_FAIL)


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
            'msg': "登录成功",
            'token': token
        }
        return render_json(data, OK)
    else:
        data = {
            'msg': '登录失败',
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
    user.id = uid  # 保存用户id
    user.icon = filename  # 用户头像文件名
    user.phone = exist_user.phone  # 用户手机号
    user.save()
    return render_json(user.to_dict(), OK)


# ===================表白===============================
def issue(request):
    '''发表表白贴子'''
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
    return render_json(confess.to_dict('release_time'), OK)


def get_self_issue(request):
    '''获取自己所有发布的表白帖子'''
    uid = request.user.id
    confessions = Confess.objects.filter(Q(userID=uid) & Q(is_delete=False))
    data = many_to_dict(confessions)
    return render_json(data, OK)


def delete_self_issue(request):
    '''删除表白帖子'''
    user = request.user
    confessid = request.GET.get("confessid")
    confess = Confess.objects.filter(pk=confessid)
    if confess.exists():
        confess = confess.first()
        if user.id == confess.userID:
            confess.is_delete = True
            confess.save()
            return render_json(confess.to_dict('release_time'), OK)
        else:
            return render_json({'msg': "没有权限删除该帖子"}, ISSUE_NOT_ALLOWED)
    else:
        return render_json({'msg': '该表白帖子不存在'}, ISSUE_NOT_EXIST)


def index(request):
    '''首页信息展示'''
    # 帖子分页
    confesses = Confess.objects.all()[1:10]
    data = many_to_dict(confesses)
    return render_json(data, OK)


def do_comment(request):
    '''评论'''
    user_id = request.user.id
    confess_id = request.GET.get('confess_id')
    context = request.POST.get('comment')
    comment = Comment()
    comment.userID = user_id
    comment.confessID = confess_id
    comment.context = context
    comment.save()
    return render_json(comment.to_dict('comment_time'), OK)


def get_comments(request):
    '''获取某条帖子的所有评论'''
    confess_id = request.GET.get('confess_id')
    comments = Comment.objects.filter(confessID=confess_id)
    data = many_to_dict()
    pass
