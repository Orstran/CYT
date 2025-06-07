from django import forms
from .models import Post, Category, Comment, About, Contact, AnimeNavigation, WebsiteNavigation

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'custom_category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入文章标题'}),
            'content': forms.Textarea(attrs={'placeholder': '请输入文章内容', 'rows': 5}),
            'tags': forms.TextInput(attrs={'placeholder': '输入标签，用逗号分隔'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_predefined']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '请输入分类名称'}),
        }

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '请输入关于我们的内容', 'rows': 5}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'phone', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': '请输入邮箱地址'}),
            'phone': forms.TextInput(attrs={'placeholder': '请输入电话号码'}),
            'address': forms.Textarea(attrs={'placeholder': '请输入地址', 'rows': 3}),
        }

class AnimeNavigationForm(forms.ModelForm):
    class Meta:
        model = AnimeNavigation
        fields = ['title', 'url', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入动漫导航标题'}),
            'url': forms.URLInput(attrs={'placeholder': '请输入链接，例如 https://example.com'}),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError('请输入有效的URL，需以 http:// 或 https:// 开头。')
        return url

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        if not title:
            raise forms.ValidationError('标题不能为空。')
        return title

class WebsiteNavigationForm(forms.ModelForm):
    class Meta:
        model = WebsiteNavigation
        fields = ['title', 'url', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入网站导航标题'}),
            'url': forms.URLInput(attrs={'placeholder': '请输入链接，例如 https://example.com'}),
            'description': forms.Textarea(attrs={'placeholder': '请输入描述，最多200字', 'rows': 3}),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError('请输入有效的URL，需以 http:// 或 https:// 开头。')
        return url

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        if not title:
            raise forms.ValidationError('标题不能为空。')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description').strip()
        if len(description) > 200:
            raise forms.ValidationError('描述不能超过200字。')
        return description

# 修改记录：
# 1. 为 AnimeNavigationForm 添加 clean_title 方法，确保标题不为空。
# 2. 为 WebsiteNavigationForm 添加 clean_title 和 clean_description 方法，确保标题不为空且描述不超过200字。
# 3. 为所有表单添加 widgets 和 placeholder 属性，提升用户体验。