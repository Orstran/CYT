from django import template
from django.forms import Field

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    为表单字段添加CSS类，支持追加现有类。

    参数：
        field：Django表单字段。
        css_class：要添加的CSS类名（可包含多个类，用空格分隔，如 "form-control mb-3"）。
    返回：
        带新CSS类的表单字段。
    异常：
        返回原始字段如果输入无效。
    """
    if not isinstance(field, Field) or not css_class:
        return field
    attrs = field.field.widget.attrs
    existing_classes = attrs.get('class', '').split()
    new_classes = css_class.split()
    combined_classes = ' '.join(set(existing_classes + new_classes))
    attrs = attrs.copy()  # Avoid modifying the original attrs
    attrs['class'] = combined_classes.strip()
    return field.as_widget(attrs=attrs)

@register.filter
def add_attrs(field, attrs_str):
    """
    为表单字段添加任意HTML属性。

    参数：
        field：Django表单字段。
        attrs_str：属性字符串，如 "placeholder='Enter title' id='custom-id'"。
    返回：
        带新属性的表单字段。
    异常：
        返回原始字段如果输入无效。
    """
    if not isinstance(field, Field) or not attrs_str:
        return field
    attrs = field.field.widget.attrs.copy()
    for attr in attrs_str.split():
        if '=' in attr:
            key, value = attr.split('=', 1)
            attrs[key.strip()] = value.strip("'").strip('"')
    return field.as_widget(attrs=attrs)

# 修改记录：
# 1. Enhanced add_class to preserve existing classes and support multiple classes.
# 2. Added add_attrs filter for adding arbitrary HTML attributes.
# 3. Added error handling and documentation for better robustness and maintainability.