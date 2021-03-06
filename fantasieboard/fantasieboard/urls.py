"""fantasieboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('community/', views.community_view, name='community'),
    path('community/<str:community_name>/', 
         views.community_article, name='community_detail'),
    path('community/<str:community_name>/<int:article_pk>/', 
         views.article_view, name='article_detail'),
    
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('community/<str:community_name>/write/', views.write_article, name='write_article'),
    path('community/<str:community_name>/<int:article_pk>/edit/', views.edit_article, name='edit_article'),
    path('community/<str:community_name>/<int:article_pk>/delete/', views.delete_article, name='delete_article'),
    path('community/<str:community_name>/<int:article_pk>/reply/', views.reply_article, name='reply_article'),
    path('community/<str:community_name>/<int:article_pk>/delete_comment/<int:comment_pk>/', 
         views.delete_comment, name='delete_comment'),
    path('community/<str:community_name>/<int:article_pk>/edit_comment/<int:comment_pk>/',
         views.edit_comment, name='edit_comment'),
    path('like/<int:article_pk>/', views.like_button, name='like_article'),
    
    path('community//', views.community_not_found_404, name='not_found_c'),
    path('community/<str:community_name>//', views.community_article, name='community_detail'),
    path('community/<str:community_name>/<int:article_pk>/delete_comment//', 
         views.article_view, name='article_detail'),
]
