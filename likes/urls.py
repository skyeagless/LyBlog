from django.urls import path
from . import views

#start with likes
urlpatterns = [
    path('like_change/',views.like_change,name='like_change'),
]
