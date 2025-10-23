from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Author, Journal, JournalMetric, Paper

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    作者模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'name',
        'email',
        'staff_link',
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
    # 只读字段
    readonly_fields = ('created_at', 'updated_at')

    def staff_link(self, obj):
        """\显示关联员工的链接"""
        if obj.staff:
            url = reverse('admin:users_staff_change', args=[obj.staff.id])
            return format_html('<a href="{}">{}</a>', url, obj.staff.name)
        return '-'

    staff_link.short_description = _('关联员工')


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """
    期刊模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'name',
        'issn',
        'current_jcr_quartile',
        'current_impact_factor',
        'paper_count',
        'created_at',
        'updated_at'
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
    # 添加表单中搜索框
    autocomplete_fields = ()

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
class PaperAdmin(admin.ModelAdmin):
    """
    论文模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'title',
        'journal_link',
        'publication_year',
        'unit_ranking',
        'first_authors_list',
        'corresponding_authors_list',
        'created_at',
        'updated_at'
    )
    # 搜索字段
    search_fields = (
        'title',
        'keywords',
        'abstract',
        'first_authors__name',
        'corresponding_authors__name',
        'journal__name'
    )
    # 过滤器
    list_filter = (
        'publication_year',
        'created_at',
        'updated_at'
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


@admin.register(JournalMetric)
class JournalMetricAdmin(admin.ModelAdmin):
    """
    期刊年度指标模型的后台管理配置
    """
    # 列表显示的字段
    list_display = (
        'journal_link',
        'year',
        'jcr_quartile',
        'impact_factor',
        'created_at',
        'updated_at'
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
    # 编辑表单的内联布局
    formfield_overrides = {
        # 自定义字段显示
    }

    def journal_link(self, obj):
        """显示关联期刊的链接"""
        if obj.journal:
            url = reverse('admin:achievement_journal_change', args=[obj.journal.id])
            return format_html('<a href="{}">{}</a>', url, obj.journal.name)
        return '-'

    journal_link.short_description = _('期刊')
