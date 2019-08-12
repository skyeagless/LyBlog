from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")

    #获得顶级评论
    root = models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name="root_comment")
    #建立评论的树结构（reply)
    parent = models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name="parent_comment")
    #回复谁（需要设置反向寻找）
    reply_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="replies")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']

