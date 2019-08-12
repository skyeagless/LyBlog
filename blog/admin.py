from django.contrib import admin
from .models import BlogType,Blog,ViewedNum,ViewedDetail

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','blog_type',"author","get_viewed_num","created_time","last_update_time")

@admin.register(ViewedNum)
class ViewedNumAdmin(admin.ModelAdmin):
    list_display = ('viewed_num','blog')

@admin.register(ViewedDetail)
class ViewedDetailAdmin(admin.ModelAdmin):
    list_display = ('date','viewed_num','blog')

