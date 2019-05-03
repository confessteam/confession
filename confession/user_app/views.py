import pdb
import uuid
from urllib.parse import urljoin

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from confession.settings import MY_STATIC_FILES_URL
from user_app.constant import OK, VERIFY_CODE_FAIL, BAD_DATA, ISSUE_NOT_EXIST, ISSUE_NOT_ALLOWED, GET_ICON_IMAGE_FAIL, \
    NO_DATA, DELETE_ADD
from user_app.logic import get_code, send_msg, render_json, check_vcode, save_upload_file, \
    many_to_dict, get_first_image_list, save_images
from user_app.models import User, Confess, Comment, Collection, Care, Notice
from user_app.verify_form import UserForm


def hello(request):
    return render(request, 'text.html')


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
    # vcode = '123123'
    vcode = get_code(4)
    res = send_msg(phonenum, vcode)
    cache.set('Vcode-%s' % phonenum, vcode, timeout=3600)
    print(cache.get('Vcode-%s' % phonenum))
    return render_json(None, OK)


def login(request):
    '''无需注册的登录，如果不存在则创建'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        user, _ = User.objects.get_or_create(phone=phonenum)
        user.u_name = phonenum
        user.save()
        token = uuid.uuid4().hex
        cache.set(token, user.id)
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
def uploadFirst(request):
    '''前端upload插件第一次访问api'''
    return HttpResponse("ok")


def uploadImg(request):
    '''发布接口'''
    userId = request.user.id
    img_file = request.FILES.getlist("file")
    fileNamesList = save_images(userId,img_file)
    host = 'http://127.0.0.1:8000/static/confessImage/'
    fileNamesList = [host + file for file in fileNamesList]
    fileNamesStr = '##'.join(fileNamesList)
    confess = Confess()
    confess.userID = userId
    confess.images = fileNamesStr
    confess.context = request.POST.get('content')
    confess.contentType = request.POST.get('info')
    confess.save()
    return render_json(data={'msg':'upload success'},code=OK)


def get_self_issue(request):
    '''获取自己所有发布的表白帖子'''
    uid = request.user.id
    confesses = Confess.objects.filter(Q(userID=uid) & Q(is_delete=False)).order_by('-id')
    if confesses.exists():
        length = len(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:length // 2]),
            'confesses2': many_to_dict(confesses[length // 2:length]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


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


def do_comment(request):
    '''评论'''
    user_id = request.user.id
    confess_id = request.POST.get('confess_id')
    confess = Confess.objects.get(pk=confess_id)
    confess.commentCount += 1
    confess.save()
    context = request.POST.get('comment')
    comment = Comment()
    comment.userID = user_id
    comment.confessID = confess_id
    comment.context = context
    comment.save()
    data = {
        'comment':comment.to_dict('comment_time'),
        'user':{
            'name':request.user.u_name
        }
    }
    return render_json(data, OK)


def get_comments(request):
    '''获取某条帖子的所有评论'''
    confess_id = request.POST.get('confess_id')
    comments = Comment.objects.filter(confessID=confess_id).order_by('-id')
    user_and_comment_list = []
    for comment in comments:
        user = User.objects.filter(pk=comment.userID)
        user_and_comment_list.append({"user":user[0].to_dict('create_time', 'action_time','birthday'), "comment":comment.to_dict('comment_time')})
    return render_json(user_and_comment_list, OK)


def add_collection(request):
    '''添加收藏'''
    userId = request.user.id
    confessionId = request.POST.get('confess_id')
    collectedUserId = request.POST.get('userId')
    collects = Collection.objects.filter(Q(userID=userId)&Q(confessID=confessionId))
    if collects:
        collects.delete()
        confess = Confess.objects.get(pk=confessionId)
        confess.collectCount -= 1
        confess.save()
        return render_json(many_to_dict(collects), DELETE_ADD)
    collection = Collection()
    collection.userID = userId
    collection.confessID = confessionId
    collection.save()
    confession = Confess.objects.get(pk=confessionId)
    confession.collectCount += 1
    confession.save()

    notice = Notice()
    notice.userId = collectedUserId
    if collectedUserId == 2:
        notice.messageType = '系统'
    notice.messageType = '用户'
    notice.messageState = '未读'
    notice.message = '%s收藏了你的作品' % request.user.u_name
    notice.save()

    return render_json(collection.to_dict(), OK)


def index(request):
    '''首页信息展示'''
    # 需要每条表白的 第一张图片、点赞数、评论数
    # 帖子分页
    start = int(request.GET.get('start', '0').strip())
    step = int(request.GET.get('step', '10').strip())
    confesses = Confess.objects.filter(contentType=1).order_by('-id')[start:step]
    if confesses.exists():
        confesses = list(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:-1:2]),
            'confesses2': many_to_dict(confesses[1:-1:2]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def get_collections(request):
    '''获取当前用户的收藏列表'''
    userId = request.user.id
    collections = Collection.objects.filter(userID=userId)
    confessIdList = [confession.confessID for confession in collections]
    confesses = Confess.objects.filter(id__in=confessIdList).order_by('-id')
    if confesses.exists():
        length = len(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:length // 2]),
            'confesses2': many_to_dict(confesses[length // 2:length]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def care(request):
    '''关注'''
    userId = request.user.id
    caredUserId = request.POST.get('userId')
    confessionId = request.POST.get('confessionId')
    cares = Care.objects.filter(Q(userID=userId) & Q(caredUserId=caredUserId))
    if cares:
        data = {
            'msg':'已关注'
        }
        return render_json(data, OK)
    attention = Care()
    attention.userID = userId
    attention.caredUserId = caredUserId
    attention.save()

    notice = Notice()
    notice.userId = caredUserId
    if caredUserId == 2:
        notice.messageType = '系统'
    notice.messageType = '用户'
    notice.messageState = '未读'
    notice.message = '%s关注了你' % request.user.u_name
    notice.save()

    return render_json(attention.to_dict(), OK)


def get_care_confessions(request):
    '''获取关注好友发布的confessions'''
    userId = request.user.id
    caredUsers = Care.objects.filter(userID=userId)
    caredUserIdList = []
    for user in caredUsers:
        caredUserIdList.append(user.caredUserId)
    confesses = Confess.objects.filter(userID__in=caredUserIdList).order_by('-id')
    if confesses.exists():
        confesses = list(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:-1:2]),
            'confesses2': many_to_dict(confesses[1:-1:2]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def get_notice(request):
    '''消息通知'''
    try:
        # 用户登录过
        userId = request.user.id
        notices = Notice.objects.filter(
            (Q(userId=userId) & Q(messageState='未读'))).order_by('-id') #Q(messageType="系统") & Q(messageState='未读')
        data = many_to_dict(notices)
        return render_json(data, OK)
    except Exception as e:
        # 用户没有登录过
        notices = Notice.objects.filter(Q(messageType="系统") & Q(messageState='未读'))
        data = many_to_dict(notices)
        return render_json(data, OK)


def get_public_notice(request):
    '''消息通知'''
    try:
        # 用户登录过
        userId = request.user.id
        userId = 3
        notices = Notice.objects.filter(
            Q(messageType="系统") & Q(messageState='未读'))  # Q(messageType="系统") & Q(messageState='未读')
        data = many_to_dict(notices)
        return render_json(data, OK)
    except Exception as e:
        # 用户没有登录过
        notices = Notice.objects.filter(Q(messageType="系统") & Q(messageState='未读'))
        data = many_to_dict(notices)
        return render_json(data, OK)


# 失物招领模块
def get_lost_and_found(request):
    '''失物招领商品数据展示'''
    confesses = Confess.objects.filter(contentType='2').order_by('-id')
    if confesses.exists():
        length = len(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:length // 2]),
            'confesses2': many_to_dict(confesses[length // 2:length]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def get_mall(request):
    '''二手商品数据展示'''
    confesses = Confess.objects.filter(contentType='3').order_by('-id')
    if confesses.exists():
        length = len(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:length // 2]),
            'confesses2': many_to_dict(confesses[length // 2:length]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def get_others(request):
    '''其他数据展示'''
    confesses = Confess.objects.filter(contentType='4').order_by('-id')
    if confesses.exists():
        length = len(confesses)
        data = {
            'confesses1': many_to_dict(confesses[0:length // 2]),
            'confesses2': many_to_dict(confesses[length // 2:length]),
        }
        return render_json(data, OK)
    else:
        data = {
            'confesses1': [],
            'confesses2': []
        }
        return render_json(data, NO_DATA)


def changeMessageState(request):
    userId = request.user.id
    noticeId = request.GET.get('messageId')
    notices = Notice.objects.filter(Q(pk=noticeId)&Q(userId=userId))
    if notices:
        notice = notices[0]
        notice.messageState = '已读'
        notice.save()
    data = {
        'message':'修改状态成功',
    }
    return render_json(data, OK)
