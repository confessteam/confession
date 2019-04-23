from django.contrib import admin

from user_app.models import User, Confess, Comment, Collection, Care, Notice


# Register your models here.

admin.site.register(User)
admin.site.register(Confess)
admin.site.register(Comment)
admin.site.register(Collection)
admin.site.register(Care)
admin.site.register(Notice)
