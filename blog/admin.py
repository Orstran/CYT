from django.contrib import admin
from .models import Post, Category, About, Contact, Comment, AnimeNavigation, WebsiteNavigation

# 文章管理配置
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'category')
    list_filter = ('category', 'created_date')
    search_fields = ('title', 'content')

# 分类管理配置
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_predefined')
    search_fields = ('name',)

# 评论管理配置
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

# 关于我们管理配置
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('updated_date',)

# 联系我们管理配置
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'updated_date')

# 热门动漫导航管理配置
@admin.register(AnimeNavigation)
class AnimeNavigationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title',)

# 常用网站导航管理配置
@admin.register(WebsiteNavigation)
class WebsiteNavigationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title',)

# 修改记录：添加了 AnimeNavigation 和 WebsiteNavigation 模型的管理员配置。