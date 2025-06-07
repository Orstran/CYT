from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # 公共页面路由 (Frontend)
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('categories/', views.categories, name='categories'),
    path('archive/', views.archive, name='archive'),
    # 密码修改路由 (Frontend)
    path('password_change/', PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
    # 头像上传路由
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),

    # 自定义管理员页面路由 (Backend)
    path('custom-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/login/', views.admin_login, name='admin_login'),
    path('custom-admin/password_change/', PasswordChangeView.as_view(template_name='blog/admin/password_change.html'), name='admin_password_change'),
    path('custom-admin/password_change/done/', PasswordChangeDoneView.as_view(template_name='blog/admin/password_change_done.html'), name='admin_password_change_done'),
    path('custom-admin/posts/', views.post_list, name='admin_post_list'),
    path('custom-admin/post/create/', views.post_create, name='admin_post_create'),
    path('custom-admin/post/<int:pk>/update/', views.post_update, name='admin_post_update'),
    path('custom-admin/post/<int:pk>/delete/', views.post_delete, name='admin_post_delete'),
    path('custom-admin/categories/', views.category_list, name='admin_category_list'),
    path('custom-admin/category/create/', views.category_create, name='admin_category_create'),
    path('custom-admin/category/<int:pk>/update/', views.category_update, name='admin_category_update'),
    path('custom-admin/category/<int:pk>/delete/', views.category_delete, name='admin_category_delete'),
    path('custom-admin/comments/', views.comment_list, name='admin_comment_list'),
    path('custom-admin/comment/<int:pk>/delete/', views.comment_delete, name='admin_comment_delete'),
    path('custom-admin/about/update/', views.about_update, name='admin_about_update'),
    path('custom-admin/contact/update/', views.contact_update, name='admin_contact_update'),
    path('custom-admin/anime-navigation/', views.anime_navigation_list, name='admin_anime_navigation_list'),
    path('custom-admin/anime-navigation/create/', views.anime_navigation_create, name='admin_anime_navigation_create'),
    path('custom-admin/anime-navigation/<int:pk>/update/', views.anime_navigation_update, name='admin_anime_navigation_update'),
    path('custom-admin/anime-navigation/<int:pk>/delete/', views.anime_navigation_delete, name='admin_anime_navigation_delete'),
    path('custom-admin/website-navigation/', views.website_navigation_list, name='admin_website_navigation_list'),
    path('custom-admin/website-navigation/create/', views.website_navigation_create, name='admin_website_navigation_create'),
    path('custom-admin/website-navigation/<int:pk>/update/', views.website_navigation_update, name='admin_website_navigation_update'),
    path('custom-admin/website-navigation/<int:pk>/delete/', views.website_navigation_delete, name='admin_website_navigation_delete'),
]

# 修改记录：
# 1. 修正语法错误，添加缺失的逗号和适当的格式。
# 2. 之前记录：添加了 upload-profile-image 路由。