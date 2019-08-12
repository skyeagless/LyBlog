from django.urls import path
from . import views

#start with comment
urlpatterns = [
    path('update_comment/',views.update_comment,name='update_comment'),
]
