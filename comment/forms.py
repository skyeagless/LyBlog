from django import forms
from blog.models import Blog
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment

class CommentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required':"评论内容不能为空"})
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

    def __init__(self,*args,**kwargs):
        #把user对象传进来，因为没有request
        ## if kwargs has no key 'user', user is assigned None
# make sure your code handles this case gracefully
        self.user = kwargs.pop('user',None)
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):
        #判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        #评论对象验证
        object_id = self.cleaned_data['object_id']
        try:
            blog = Blog.objects.get(id=object_id)
            self.cleaned_data['blog'] = blog
        except ObjectDoesNotExist:
            raise forms.ValidationError("评论对象不存在")
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError("回复出错")
        return reply_comment_id



