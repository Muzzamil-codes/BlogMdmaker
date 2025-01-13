from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login, name="login"),
    path("user_panel/", userpanel, name="userpanel"),
    path('logout/', logout_view, name="logout_view"),
    # path('blog_detail/<slug>', blog_detail, name="blog_detail"),
    path("add_blog/", add_blog, name="add_blog"),
    path('update_blog/<slug>/', update_blog, name="update_blog"),
    path("blog_delete/<slug>/", delete_blog, name="delete_blog"),
    path("reset_password", reset_password, name="reset_password")
]