"""定制site，用户模块与文章、分类等模块的管理分离"""
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typediea'
    site_title = 'Typediea管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
