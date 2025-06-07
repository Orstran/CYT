from django import template

register = template.Library()

@register.inclusion_tag('blog/comment_thread.html', takes_context=True)
def render_comments(context, parent_comments, replies_dict):
    return {
        'parent_comments': parent_comments,
        'replies_dict': replies_dict,
        'request': context['request'],
        'post': context['post'],
    }

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])  # Return empty list if key not found, no string conversion

# 修改记录：
# 1. 新建 comment_tags.py 文件，定义 render_comments 模板标签。
# 2. 支持递归渲染嵌套评论，通过 level 参数控制缩进。
# 3. 传递 request 和 post 上下文，确保模板可以访问用户认证状态和文章信息。
# 4. 修改 render_comments 标签，移除 level 参数，改为传递 parent_comments 和 replies_dict，支持两级评论结构。
# 5. 添加 get_item 自定义过滤器，用于在模板中安全地从字典中获取键对应的值。
# 6. 修改 get_item 过滤器，移除 str(key) 转换，直接使用原始键，并返回空列表作为默认值，防止 None 值导致模板渲染问题。