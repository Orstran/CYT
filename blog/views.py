from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CommentForm, PostForm, CategoryForm, AboutForm, ContactForm, AnimeNavigationForm, WebsiteNavigationForm
from .models import Post, Category, About, Contact, Comment, AnimeNavigation, WebsiteNavigation, UserProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

# Custom decorator to ensure user is a superuser
def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "您需要使用超级账户登录才能访问后台管理系统。")
            return redirect('admin_login')
        if not request.user.is_superuser:
            messages.error(request, "您没有权限访问此页面。请使用超级账户登录。")
            return render(request, 'blog/admin/permission_denied.html', {'next': request.path})
        return view_func(request, *args, **kwargs)
    return wrapper

# 首页视图：显示分页的文章列表 (Frontend)
def home(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    anime_navs = AnimeNavigation.objects.all().order_by('-created_at')[:3]
    website_navs = WebsiteNavigation.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'anime_navs': anime_navs,
        'website_navs': website_navs
    })

# 头像上传视图
@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
                profile.save()
                messages.success(request, "头像上传成功！")
            else:
                messages.error(request, "请选择一个图片文件。")
        except Exception as e:
            messages.error(request, f"上传失败：{str(e)}")
    return redirect('home')

# 用户注册视图 (Frontend)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect('home')
        else:
            messages.error(request, "注册失败，请检查输入。")
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

# 用户登录视图 (Frontend)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "登录失败，请检查用户名和密码。")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

# 管理员登录视图 (Backend)
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "仅超级账户可以访问后台管理系统。")
        else:
            messages.error(request, "登录失败，请检查用户名和密码。")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/admin/admin_login.html', {'form': form})

# 用户登出视图
def logout_view(request):
    logout(request)
    if request.path.startswith('/custom-admin/'):
        messages.success(request, "您已成功退出后台管理系统。")
        return redirect('admin_login')
    else:
        messages.success(request, "您已成功退出。")
        return redirect('home')

# 文章详情视图：显示文章及相关评论 (Frontend)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
    print(f"Debug - parent_comments for post {pk}: {[comment.id for comment in parent_comments]}")  # Debug parent comment IDs
    # Fetch all replies and flatten them under their top-level parent
    replies_dict = {}
    for parent in parent_comments:
        replies = []
        def collect_replies(comment):
            for reply in comment.replies.all().order_by('created_at'):
                replies.append(reply)
                collect_replies(reply)
        collect_replies(parent)
        replies_dict[parent.id] = replies
    print(f"Debug - replies_dict for post {pk}: {replies_dict}")
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'parent_comments': parent_comments,
        'replies_dict': replies_dict
    })

# 发布新文章视图（需登录） (Frontend)
@login_required
def post_new(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST.get('category')
        custom_category = request.POST.get('custom_category', '').strip()
        tags = request.POST.get('tags', '').strip()
        author = request.user

        if not title or not content:
            messages.error(request, "标题和内容不能为空。")
            categories = Category.objects.filter(is_predefined=True)
            return render(request, 'blog/post_new.html', {'categories': categories})

        try:
            category = Category.objects.get(id=category_id) if category_id else \
                Category.objects.get_or_create(name=custom_category or "Uncategorized", is_predefined=False)[0]
            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
                category=category,
                custom_category=custom_category if custom_category else None,
                tags=tags
            )
            messages.success(request, "文章发布成功！")
            return redirect('home')
        except Category.DoesNotExist:
            messages.error(request, "选择的分类不存在。")
            categories = Category.objects.filter(is_predefined=True)
            return render(request, 'blog/post_new.html', {'categories': categories})
    else:
        categories = Category.objects.filter(is_predefined=True)
        return render(request, 'blog/post_new.html', {'categories': categories})

# 添加评论视图 (Frontend)
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated:
        messages.error(request, "请登录后发表评论。")
        return redirect('login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content'].strip()
            if not content:
                messages.error(request, "评论内容不能为空。")
                return redirect('post_detail', pk=post_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, post=post)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    messages.error(request, "回复的评论不存在。")
                    return redirect('post_detail', pk=post_id)
            comment.save()
            messages.success(request, "评论发布成功！")
        else:
            messages.error(request, "评论发布失败，请检查输入。")
    return redirect('post_detail', pk=post_id)

# 关于我们页面 (Frontend)
def about(request):
    about = About.objects.first()
    if not about:
        about = About.objects.create(content="欢迎访问我们的博客系统！这里是关于我们的介绍。")
    return render(request, 'blog/about.html', {'about': about})

# 联系我们页面 (Frontend)
def contact(request):
    contact = Contact.objects.first()
    if not contact:
        contact = Contact.objects.create(email="contact@blog.com", phone="", address="北京市海淀区")
    return render(request, 'blog/contact.html', {'contact': contact})

# 分类列表页面 (Frontend)
def categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})

# 文章归档页面 (Frontend)
def archive(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'blog/archive.html', {'posts': posts})

# 管理仪表板（需登录且为超级用户）
@superuser_required
def admin_dashboard(request):
    return render(request, 'blog/admin/dashboard.html')

# 文章管理列表（需登录且为超级用户）
@superuser_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/admin/post_list.html', {'page_obj': page_obj})

# 创建文章（管理员，需登录且为超级用户）
@superuser_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "文章创建成功！")
            return redirect('admin_post_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = PostForm()
    return render(request, 'blog/admin/post_create.html', {'form': form})

# 更新文章（管理员，需登录且为超级用户）
@superuser_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "文章更新成功！")
            return redirect('admin_post_list')
        else:
            messages.error(request, "更新失败，请检查输入。")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/admin/post_update.html', {'form': form, 'post': post})

# 删除文章（管理员，需登录且为超级用户）
@superuser_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "文章删除成功！")
        return redirect('admin_post_list')
    return render(request, 'blog/admin/post_delete.html', {'post': post})

# 分类管理列表（需登录且为超级用户）
@superuser_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/admin/category_list.html', {'categories': categories})

# 创建分类（管理员，需登录且为超级用户）
@superuser_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "分类创建成功！")
            return redirect('admin_category_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = CategoryForm()
    return render(request, 'blog/admin/category_create.html', {'form': form})

# 更新分类（管理员，需登录且为超级用户）
@superuser_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "分类更新成功！")
            return redirect('admin_category_list')
        else:
            messages.error(request, "更新失败，请检查输入。")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/admin/category_update.html', {'form': form, 'category': category})

# 删除分类（管理员，需登录且为超级用户）
@superuser_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "分类删除成功！")
        return redirect('admin_category_list')
    return render(request, 'blog/admin/category_delete.html', {'category': category})

# 评论管理列表（需登录且为超级用户）
@superuser_required
def comment_list(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'blog/admin/comment_list.html', {'comments': comments})

# 删除评论（管理员，需登录且为超级用户）
@superuser_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "评论删除成功！")
        return redirect('admin_comment_list')
    return render(request, 'blog/admin/comment_delete.html', {'comment': comment})

# 更新关于我们（管理员，需登录且为超级用户）
@superuser_required
def about_update(request):
    about = About.objects.first()
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "关于我们更新成功！")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "更新失败，请检查输入。")
    else:
        form = AboutForm(instance=about)
    return render(request, 'blog/admin/about_update.html', {'form': form})

# 更新联系我们（管理员，需登录且为超级用户）
@superuser_required
def contact_update(request):
    contact = Contact.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "联系我们更新成功！")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "更新失败，请检查输入。")
    else:
        form = ContactForm(instance=contact)
    return render(request, 'blog/admin/contact_update.html', {'form': form})

# 热门动漫导航管理列表（需登录且为超级用户）
@superuser_required
def anime_navigation_list(request):
    anime_navs = AnimeNavigation.objects.all().order_by('-created_at')
    paginator = Paginator(anime_navs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/admin/anime_navigation_list.html', {'page_obj': page_obj})

# 创建热门动漫导航（管理员，需登录且为超级用户）
@superuser_required
def anime_navigation_create(request):
    if request.method == 'POST':
        form = AnimeNavigationForm(request.POST, request.FILES)
        if form.is_valid():
            anime_nav = form.save()
            messages.success(request, f"动漫导航“{anime_nav.title}”创建成功！")
            return redirect('admin_anime_navigation_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = AnimeNavigationForm()
    return render(request, 'blog/admin/anime_navigation_create.html', {'form': form})

# 更新热门动漫导航（管理员，需登录且为超级用户）
@superuser_required
def anime_navigation_update(request, pk):
    anime_nav = get_object_or_404(AnimeNavigation, pk=pk)
    if request.method == 'POST':
        form = AnimeNavigationForm(request.POST, request.FILES, instance=anime_nav)
        if form.is_valid():
            anime_nav = form.save()
            messages.success(request, f"动漫导航“{anime_nav.title}”更新成功！")
            return redirect('admin_anime_navigation_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = AnimeNavigationForm(instance=anime_nav)
    return render(request, 'blog/admin/anime_navigation_update.html', {'form': form, 'anime_nav': anime_nav})

# 删除热门动漫导航（管理员，需登录且为超级用户）
@superuser_required
def anime_navigation_delete(request, pk):
    anime_nav = get_object_or_404(AnimeNavigation, pk=pk)
    if request.method == 'POST':
        title = anime_nav.title
        anime_nav.delete()
        messages.success(request, f"动漫导航“{title}”删除成功！")
        return redirect('admin_anime_navigation_list')
    return render(request, 'blog/admin/anime_navigation_delete.html', {'anime_nav': anime_nav})

# 常用网站导航管理列表（需登录且为超级用户）
@superuser_required
def website_navigation_list(request):
    website_navs = WebsiteNavigation.objects.all().order_by('-created_at')
    paginator = Paginator(website_navs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/admin/website_navigation_list.html', {'page_obj': page_obj})

# 创建常用网站导航（管理员，需登录且为超级用户）
@superuser_required
def website_navigation_create(request):
    if request.method == 'POST':
        form = WebsiteNavigationForm(request.POST)
        if form.is_valid():
            website_nav = form.save()
            messages.success(request, f"网站导航“{website_nav.title}”创建成功！")
            return redirect('admin_website_navigation_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = WebsiteNavigationForm()
    return render(request, 'blog/admin/website_navigation_create.html', {'form': form})

# 更新常用网站导航（管理员，需登录且为超级用户）
@superuser_required
def website_navigation_update(request, pk):
    website_nav = get_object_or_404(WebsiteNavigation, pk=pk)
    if request.method == 'POST':
        form = WebsiteNavigationForm(request.POST, instance=website_nav)
        if form.is_valid():
            form.save()
            messages.success(request, f"网站导航“{website_nav.title}”更新成功！")
            return redirect('admin_website_navigation_list')
        else:
            messages.error(request, "创建失败，请检查输入。")
    else:
        form = WebsiteNavigationForm(instance=website_nav)
    return render(request, 'blog/admin/website_navigation_update.html', {'form': form, 'website_nav': website_nav})

# 删除常用网站导航（管理员，需登录且为超级用户）
@superuser_required
def website_navigation_delete(request, pk):
    website_nav = get_object_or_404(WebsiteNavigation, pk=pk)
    if request.method == 'POST':
        website_nav.delete()
        messages.success(request, "网站导航删除成功！")
        return redirect('admin_website_navigation_list')
    return render(request, 'blog/admin/website_navigation_delete.html', {'website_nav': website_nav})

# 修改记录：
# 1. 优化 add_comment 视图，增强对 parent_id 的处理，确保支持任意层级的嵌套评论。
# 2. 添加更严格的空内容检查和错误提示。
# 3. 使用 try-except 捕获 parent_id 不存在的情况，防止无效回复。
# 4. 添加未登录用户的提示消息，引导用户登录。
# 5. 保持原有的成功消息和重定向逻辑。
# 6. 之前记录：添加 upload_profile_image 视图处理头像上传逻辑。
# 7. 修改 post_detail 视图，传递 parent_comments 和 replies_dict，支持两级评论结构（一级为父评论，二级为所有回复）。
# 8. 优化 post_detail 视图中的 replies_dict 逻辑，使用递归函数 collect_replies，确保所有嵌套回复都展平到父评论下。
# 9. 添加 debug 打印语句以检查 replies_dict 的内容，排查回复未显示的问题。
# 10. 添加 debug 打印语句以检查 parent_comments 的 ID，确保父评论与 replies_dict 匹配。
# 11. 恢复 anime_navigation_list 视图，修复 AttributeError 错误。