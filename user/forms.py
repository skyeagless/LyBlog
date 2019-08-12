from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label="新昵称",max_length=20,widget=forms.TextInput(
        attrs={'class':"form-control","placeholder":"请输入新昵称"}))

    def __init__(self, *args, **kwargs):
        # 把user对象传进来，因为没有request
        ## if kwargs has no key 'user', user is assigned None
        # make sure your code handles this case gracefully
        self.user = kwargs.pop('user', None)
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise forms.ValidationError("昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(
        attrs={'class': "form-control", "placeholder": "请输入邮箱"}))
    verification = forms.CharField(label="验证码",required=False,widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "点击（发送验证码）到邮箱"}))

    def __init__(self, *args, **kwargs):
        # 把user对象传进来，因为没有request
        ## if kwargs has no key 'user', user is assigned None
        # make sure your code handles this case gracefully
        self.request = kwargs.pop('request', None)
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        #判断用户是否已经绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定过了邮箱')
        #判断验证码
        code = self.request.session.get('bind_email_code','')
        verification = self.cleaned_data.get('verification','')
        if not (code != '' and code == verification):
            raise forms.ValidationError('验证不通过')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经绑定')
        return email

    def clean_verification(self):
        verification = self.cleaned_data.get('verification', '').strip()
        if verification == '':
            raise forms.ValidationError("邮箱不能为空")
        return verification


