from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType,ViewedNum,ViewedDetail
from django.core.paginator import Paginator
from django.conf import settings
from LyOnline.forms import LoginForm
from django.utils import timezone
from comment.models import Comment
from comment.forms import CommentForm
from likes.models import LikeRecord

def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.BLOGS_NUMBER_EACH_PAGE)
    # 获取页码参数（GET请求）
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)  # 内部得到页码页面

    cur_page_num = page_of_blogs.number  # 获取当前页码
    page_range = list(range(max(cur_page_num - 2, 1), min(cur_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获得日期归档对应的数量，由于其是datetime变量，所以比较麻烦
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict = {} #日期(key)---数量(value)
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    content = {}
    content['blogs'] = page_of_blogs.object_list
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blog_types'] = BlogType.objects.all()
    content["blog_dates"] = blog_dates_dict
    return content

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    content = get_blog_list_common_data(request,blogs_all_list)
    return render(request,"blog_list.html",content)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    content = get_blog_list_common_data(request,blogs_all_list)
    content["blog_type"] = blog_type
    return render(request,'blog_with_types.html',content)

def blogs_with_date(request,year,month):
    #得到对应当前年月的列表
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    content = get_blog_list_common_data(request,blogs_all_list)
    content["blogs_with_date"] = '%s年%s月'% (year,month)
    return render(request,'blog_with_dates.html', content)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)  # 当前博客
    #只得到评论，不得到回复
    comments = Comment.objects.filter(blog=blog,parent=None)
    #利用cookie防止重复计数
    if not request.COOKIES.get('blog_%s_readed'% blog_pk):
        viewednum = ViewedNum.objects.get_or_create(blog=blog)[0]
        viewednum.viewed_num += 1
        viewednum.save()
    #对于每天的数据我们也需要进行计数哦！
        vieweddetail = ViewedDetail.objects.get_or_create(date=timezone.now(),blog=blog)[0]
        vieweddetail.viewed_num += 1
        vieweddetail.save()

    content = {}
    content['content'] = get_object_or_404(Blog,pk=blog_pk)
    #上一篇博客
    content['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    content['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    content['comments'] = comments.order_by('-comment_time')
    content['comment_form'] = CommentForm(initial={'object_id':blog_pk,'reply_comment_id':0})
    #获取评论数目
    content['comments_count'] = Comment.objects.filter(blog=blog).count()
    #获取该用户是否点赞
    try:
        content['is_like'] = LikeRecord.objects.filter(blog=blog, user=request.user).exists()
    except:
        content['is_like'] = False
    #获得loginform
    content['login_form'] = LoginForm()
    response = render(request,'blog_detail.html',content)
    #存一下cookie
    response.set_cookie('blog_%s_readed'% blog_pk,'true')
    return response












