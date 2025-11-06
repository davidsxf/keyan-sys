from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Author, Journal, JournalMetric, Paper
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# 定义资源类
class AuthorResource(resources.ModelResource):
    """作者模型的资源类，用于导入导出"""
    class Meta:
        model = Author
        fields = ('id', 'name', 'email', 'staff', 'external_organization')

class JournalResource(resources.ModelResource):
    """期刊模型的资源类，用于导入导出"""
    class Meta:
        model = Journal
        fields = ('id', 'name', 'issn')

class JournalMetricResource(resources.ModelResource):
    """期刊指标模型的资源类，用于导入导出"""
    class Meta:
        model = JournalMetric
        fields = ('id', 'journal', 'year', 'jcr_quartile', 'impact_factor')

class PaperResource(resources.ModelResource):
    """论文模型的资源类，用于导入导出"""
    class Meta:
        model = Paper
        fields = ('id', 'title', 'journal', 'publication_year', 'unit_ranking', 'page_numbers', 'keywords', 'abstract')

@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    """作者模型的后台管理配置"""
    resource_class = AuthorResource
    # 列表显示的字段
    list_display = (
        'id',
        'name',
        'email',
        'staff',
        'external_organization',
        'created_at',
        'updated_at'
    )
    # 搜索字段
    search_fields = ('name', 'email', 'external_organization')
    # 过滤器
    list_filter = ('created_at', 'updated_at')
    # 排序字段
    ordering = ('name',)
    # 详细页面的字段分组
    fieldsets = (
        (
            _('基本信息'),
            {
                'fields': ('name', 'email', 'external_organization')
            }
        ),
        (
            _('关联信息'),
            {
                'fields': ('staff',)
            }
        ),
        (
            _('系统信息'),
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),  # 可折叠
            }
        ),
    )
    # 添加表单中搜索框
    autocomplete_fields = ('staff',)

@admin.register(Journal)
class JournalAdmin(ImportExportModelAdmin):
    resource_class = JournalResource
    """
    期刊模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'id', 'name', 'issn', 'current_jcr_quartile', 
        'current_impact_factor', 'paper_count', 'created_at', 'updated_at'
    )
    # 搜索字段
    search_fields = ('name', 'issn')
    # 过滤器
    list_filter = ('created_at', 'updated_at')
    # 排序字段
    ordering = ('name',)
    # 详细页面的字段分组
    fieldsets = (
        (
            _('基本信息'),
            {
                'fields': ('name', 'issn')
            }
        ),
        (
            _('系统信息'),
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            }
        ),
    )
    # 只读字段
    readonly_fields = ('created_at', 'updated_at', 'paper_count')
    
    def paper_count(self, obj):
        """显示该期刊的论文数量"""
        count = obj.papers.count()
        url = reverse('admin:achievement_paper_changelist') + f'?journal__id={obj.id}'
        return format_html('<a href="{}">{}</a>', url, count)
    
    paper_count.short_description = _('论文数量')
    
    def current_jcr_quartile(self, obj):
        """显示最新的JCR分区信息"""
        latest_metric = obj.get_latest_metric()
        return latest_metric.jcr_quartile if latest_metric else '-'    
    
    current_jcr_quartile.short_description = _('最新JCR分区')
    
    def current_impact_factor(self, obj):
        """显示最新的影响因子信息"""
        latest_metric = obj.get_latest_metric()
        return latest_metric.impact_factor if latest_metric else '-'    
    
    current_impact_factor.short_description = _('最新影响因子')

@admin.register(JournalMetric)
class JournalMetricAdmin(ImportExportModelAdmin):
    resource_class = JournalMetricResource
    """
    期刊年度指标模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'id', 'journal_link', 'year', 'jcr_quartile', 
        'impact_factor', 'created_at', 'updated_at'
    )
    # 搜索字段
    search_fields = ('journal__name', 'year')
    # 过滤器
    list_filter = ('year', 'jcr_quartile', 'created_at', 'updated_at')
    # 排序字段
    ordering = ('-year', 'journal__name')
    # 详细页面的字段分组
    fieldsets = (
        (
            _('基本信息'),
            {
                'fields': ('journal', 'year', 'jcr_quartile', 'impact_factor')
            }
        ),
        (
            _('系统信息'),
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            }
        ),
    )
    # 只读字段
    readonly_fields = ('created_at', 'updated_at')
    # 添加表单中搜索框
    autocomplete_fields = ('journal',)
    
    def journal_link(self, obj):
        """显示关联期刊的链接"""
        if obj.journal:
            url = reverse('admin:achievement_journal_change', args=[obj.journal.id])
            return format_html('<a href="{}">{}</a>', url, obj.journal.name)
        return '-'    
    
    journal_link.short_description = _('期刊')

class FirstAuthorInline(admin.TabularInline):
    """\内联编辑第一作者"""
    model = Paper.first_authors.through
    verbose_name = _('第一作者')
    verbose_name_plural = _('第一作者/共一作者')
    extra = 1
    autocomplete_fields = ('author',)


class CorrespondingAuthorInline(admin.TabularInline):
    """\内联编辑通讯作者"""
    model = Paper.corresponding_authors.through
    verbose_name = _('通讯作者')
    verbose_name_plural = _('通讯作者/共同通讯作者')
    extra = 1
    autocomplete_fields = ('author',)


@admin.register(Paper)
class PaperAdmin(ImportExportModelAdmin):
    resource_class = PaperResource
    """
    论文模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'id', 'title', 'journal_link', 'publication_year', 
        'unit_ranking', 'first_authors_list', 'corresponding_authors_list', 'created_at', 'updated_at'
    )
    # 搜索字段
    search_fields = (
        'title', 'abstract', 'keywords',
        'first_authors__name', 'corresponding_authors__name', 'journal__name'
    )
    # 过滤器
    list_filter = (
        'journal', 'publication_year', 'created_at', 'updated_at'
    )
    # 排序字段
    ordering = ('-publication_year', 'title')
    # 详细页面的字段分组
    fieldsets = (
        (
            _('基本信息'),
            {
                'fields': ('title', 'journal', 'publication_year', 'unit_ranking', 'page_numbers')
            }
        ),
        (
            _('内容信息'),
            {
                'fields': ('keywords', 'abstract'),
                'classes': ('collapse',),
            }
        ),
        (
            _('系统信息'),
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            }
        ),
    )
    # 只读字段
    readonly_fields = ('created_at', 'updated_at')
    # 排除多对多字段，因为使用了内联
    exclude = ('first_authors', 'corresponding_authors')
    # 添加内联编辑
    inlines = [FirstAuthorInline, CorrespondingAuthorInline]
    # 添加表单中搜索框
    autocomplete_fields = ('journal',)
    
    def journal_link(self, obj):
        """\显示关联期刊的链接"""
        if obj.journal:
            url = reverse('admin:achievement_journal_change', args=[obj.journal.id])
            return format_html('<a href="{}">{}</a>', url, obj.journal.name)
        return '-'    

    journal_link.short_description = _('期刊')

    def first_authors_list(self, obj):
        """\显示第一作者列表"""
        authors = obj.first_authors.all()
        return ', '.join([author.name for author in authors])

    first_authors_list.short_description = _('第一作者')

    def corresponding_authors_list(self, obj):
        """\显示通讯作者列表"""
        authors = obj.corresponding_authors.all()
        return ', '.join([author.name for author in authors])

    corresponding_authors_list.short_description = _('通讯作者')


# 删除了重复的模型注册，所有模型现在只注册一次，并保留了ImportExportModelAdmin功能
