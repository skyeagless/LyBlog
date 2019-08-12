from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions
from django.utils import timezone


#博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name
    #获取博客分类下的文章总数
    def blog_count(self):
        return self.blog_set.count()

#由于1v1的关系，因此含有viewednum这一个方法
class Blog(models.Model):
    title = models.CharField(max_length = 50)
    blog_type = models.ForeignKey(BlogType,on_delete= models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now_add = True)
    last_update_time = models.DateTimeField(auto_now = True)

    def get_viewed_num(self):
        try:
            return self.viewednum.viewed_num
        except exceptions.ObjectDoesNotExist as e:
            return 0

    def get_comments_num(self):
        from comment.models import Comment
        return Comment.objects.filter(blog=self).count()

    def get_like_num(self):
        try:
            return self.likecount.liked_num
        except exceptions.ObjectDoesNotExist as e:
            return 0

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-created_time']

#每篇博客的阅读总数量
class ViewedNum(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, default='')
    viewed_num = models.IntegerField(default=0)

#按日期的阅读数量
class ViewedDetail(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,default='')
    date = models.DateField(default=timezone.now)
    viewed_num = models.IntegerField(default=0)

