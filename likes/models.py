from django.db import models
from blog.models import Blog
from django.contrib.auth.models import User

#每一篇博客被点赞的数目
class LikeCount(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
    liked_num = models.IntegerField(default=0)

#每一个点赞是谁点的，然后点的时间和对象
class LikeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)



