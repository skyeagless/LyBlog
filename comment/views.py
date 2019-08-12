from django.shortcuts import render,reverse,redirect
from .models import Comment
from blog.models import Blog
from .forms import CommentForm
from django.http import JsonResponse
from django.utils.timezone import localtime

def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.blog = comment_form.cleaned_data['blog']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            #如果parent.root存在的话
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()
        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = localtime(comment.comment_time).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


