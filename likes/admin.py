from django.contrib import admin
from .models import LikeCount,LikeRecord

# Register your models here.
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('blog','liked_num')

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('user','blog','liked_time')


