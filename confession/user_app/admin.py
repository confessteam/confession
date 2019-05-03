from django.contrib import admin

from user_app.models import User, Confess, Comment, Collection, Care, Notice

admin.site.site_header = '我帮你后台管理系统'
admin.site.site_title = '我帮你'


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示多少条
    ordering = ('id',)  # 排序（'-id'）
    actions_on_top = True  # 顶部操作显示
    actions_on_bottom = True  # 底部操作显示
    actions_selection_counter = True  # 选中条数显示
    empty_value_display = ' -空白- '  # 空白字段显示格式
    # list_editable = ['userId', 'messageType', 'message']


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ('id', 'u_name', 'password','phone', 'icon', 'sex', 'city', 'province', 'school', 'action_time','create_time', 'birthday', 'signature') # 显示字段
    search_fields = ('id', 'u_name', 'passWord','phone', 'icon', 'sex', 'city', 'province', 'school', 'action_time','create_time', 'birthday', 'signature') # 搜索条件配置
    list_filter = ('u_name',) # 过滤字段配置


@admin.register(Confess)
class ConfessAdmin(BaseAdmin):
    list_display = ('id', 'userID', 'userName','context', 'state', 'release_time', 'contentType', 'collectCount', 'commentCount', 'likeCount','is_delete') # 显示字段
    search_fields = ('id', 'userID', 'userName','context', 'state', 'release_time', 'images', 'contentType', 'collectCount', 'commentCount', 'likeCount','is_delete') # 搜索条件配置
    list_filter = ('is_delete',) # 过滤字段配置


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('id', 'userID', 'confessID', 'context', 'comment_time', 'is_delete') # 显示字段
    search_fields = ('id', 'userID', 'confessID', 'context', 'comment_time', 'is_delete') # 搜索条件配置
    list_filter = ('is_delete',) # 过滤字段配置


@admin.register(Collection)
class CollectionAdmin(BaseAdmin):
    list_display = ('id', 'userID', 'confessID', 'is_delete') # 显示字段
    search_fields = ('id', 'userID', 'confessID', 'is_delete') # 搜索条件配置
    list_filter = ('is_delete',) # 过滤字段配置


@admin.register(Care)
class CareAdmin(BaseAdmin):
    list_display = ('id', 'userID', 'caredUserId', 'is_delete') # 显示字段
    search_fields = ('id', 'userID', 'caredUserId', 'is_delete') # 搜索条件配置
    list_filter = ('is_delete',) # 过滤字段配置


@admin.register(Notice)
class NoticeAdmin(BaseAdmin):
    list_display = ('id', 'userId', 'messageType', 'message') # 显示字段
    list_filter = ('userId', 'messageType') # 过滤字段配置
    search_fields = ('userId', 'messageType', 'message') # 搜索条件配置




