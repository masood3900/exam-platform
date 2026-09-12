import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="fix_image_urls")
def fix_image_urls(html):
    """اصلاح URL عکس‌های نسبی در HTML"""
    if not html:
        return ""

    html_str = str(html)

    # تبدیل مسیرهای نسبی به مطلق
    # مثال: ../../../media/... → /media/...
    # مثال: /accounts/media/... → /media/...
    
    # حذف ../ ها
    html_str = re.sub(r'(\.\./)+', '/', html_str)
    
    # اصلاح /accounts/media/ → /media/
    html_str = re.sub(r'/accounts/media/', '/media/', html_str)
    
    # اصلاح // های اضافی
    html_str = re.sub(r'(?<!:)//+', '/', html_str)
    
    return mark_safe(html_str)
