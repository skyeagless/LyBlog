from django.shortcuts import render,redirect,reverse
from blog.models import ViewedDetail,Blog
from django.utils import timezone
import datetime,random,string,time
from django.db.models import Sum,Case,When
from django.contrib import auth
from .forms import LoginForm,RegisterForm
from user.forms import ChangeNicknameForm,BindEmailForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from user.models import Profile
from django.core.mail import send_mail

def get_seven_day_view():
    today = timezone.now().date()
    viewed_list = []
    date_list = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        viewed_detail = ViewedDetail.objects.filter(date=date)
        tmp = 0
        try:
            for k in viewed_detail:
                tmp += k.viewed_num
        except:
            tmp = 0
        viewed_list.append(tmp)
        date_list.append(date.strftime('%m/%d'))
    return viewed_list,date_list

def get_today_hot_data():
    today = timezone.now().date()
    hot_today_data = ViewedDetail.objects.filter(date=today).order_by("-viewed_num")[:3]
    return hot_today_data

def get_yesterday_hot_data():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    hot_yesterday_data = ViewedDetail.objects.filter(date=yesterday).order_by("-viewed_num")[:3]
    return hot_yesterday_data

def get_7_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    hot_7_data = ViewedDetail.objects.filter(date__lt=today,date__gte=date).values('blog')\
                     .annotate(viewed_sum=Sum("viewed_num")).order_by("-viewed_sum")[:3]
    #hot_7_data是一个字典构成的querySet:<QuerySet [{'blog': 7, 'viewed_sum': 23}, {'blog': 11, 'viewed_sum': 18}, {'blog': 6, 'viewed_sum': 4}]>
    hot_7_blog_list = []
    viewed_sum_list = []
    for dicts in hot_7_data:
        hot_7_blog_list.append(dicts['blog'])
        viewed_sum_list.append(dicts['viewed_sum'])
    #需要根据blog_id值反查对应的Blog并返回,但要注意保持list的顺序,然后组装成一个字典
    preserved = Case(*[When(pk=pk,then=pos) for pos,pk in enumerate(hot_7_blog_list)])
    hot_7_blog = list(Blog.objects.filter(id__in=hot_7_blog_list).order_by(preserved))
    hot_7_dict = dict(zip(hot_7_blog,viewed_sum_list))
    #print(hot_7_dict)
    return hot_7_dict

def home(request):
    viewed_list,date_list = get_seven_day_view()
    hot_today_data = get_today_hot_data()
    hot_yesterday_data = get_yesterday_hot_data()
    hot_7_dict = get_7_hot_data()
    return render(request,"index.html",{
        "viewed_nums":viewed_list,
        "date_list":date_list,
        "hot_today_data":hot_today_data,
        "hot_yesterday_data":hot_yesterday_data,
        "hot_7_dict": hot_7_dict,
    })

def login(request):
    #使用Form来做（提交POST，页面加载get)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        #is_valid()合法后的逻辑处理，验证后的数据保存在实例化后返回的cleaned_data中，cleaned_data是个字典的数据格式
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    return render(request,'login.html',{ "login_form":login_form, })

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    # 使用Form来做（提交POST，页面加载get)
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        # is_valid()合法后的逻辑处理，验证后的数据保存在实例化后返回的cleaned_data中，cleaned_data是个字典的数据格式
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password_again']
            #创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            #注册完成之后直接跳转到登录页面
            return redirect(reverse('login'))
    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {"register_form": register_form, })

def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))

def user_info(request):
    return render(request,'user_info.html')

def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    return render(request,'user_form.html',{
        "form": form,
        "page_title":'修改昵称',
        "form_title": '修改昵称',
        "submit_text":'修改',
        "return_back_url": redirect_to,
    })

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    return render(request, 'bind_email.html', {
        "form": form,
        "page_title": '绑定邮箱',
        "form_title": '绑定邮箱',
        "submit_text": '绑定',
        "return_back_url": redirect_to,
    })

def send_verification_code(request):
    email = request.GET.get('email','')
    data={}
    if email:
        code = ''.join(random.sample(string.ascii_letters+string.digits),4)
        request.session['bind_email_code'] = code
        send_mail(
            '绑定邮箱',
            '验证码:%s' % code,
            '1516018513@qq/.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)



