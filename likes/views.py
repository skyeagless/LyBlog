from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount,LikeRecord
from blog.models import Blog

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

# Create your views here.
def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you are not in login state')
    object_id = request.GET.get('object_id')
    try:
        blog = Blog.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'blog object not exist')


    #该用户未点赞过，创建新record,然后加1
    if request.GET.get('is_like') == 'true':
        like_record,created =  LikeRecord.objects.get_or_create(blog=blog, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(blog=blog)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')

    #取消点赞，把对象删除，然后count-1
    else:
        if LikeRecord.objects.filter(blog=blog, user=user).exists():
            like_record = LikeRecord.objects.get(blog=blog, user=user)
            like_record.delete()
            like_count = LikeCount.objects.get(blog=blog)
            like_count.liked_num -= 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            return ErrorResponse(403,'you not like')




