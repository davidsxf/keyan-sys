from django.db import models
from core.models import Category, Org
from users.models import Staff

from django.utils.translation import gettext_lazy as _




# 项目状态选项
class ProjectStatus(models.TextChoices):
    APPROVED = "APPROVED", _("已立项")
    IN_PROGRESS = "IN_PROGRESS", _("在研")
    TERMINATED = "TERMINATED", _("终止")
    COMPLETED = "COMPLETED", _("已完成")




# 承担方式选择
class UndertakeType(models.TextChoices):
    HOST = "HOST", _("主持")
    PARTICIPATE = "PARTICIPATE", _("参加")
    COLLABORATE = "COLLABORATE", _("协作")




# 项目类型选项（如果不使用外键关联Category模型，可直接使用此选项）
class ProjectType(models.TextChoices):
    RESEARCH = "research", _("研究项目")
    DEVELOPMENT = "development", _("开发项目")
    CONSULTING = "consulting", _("咨询项目")
    SERVICE = "service", _("服务项目")
    OTHER = "other", _("其他项目")




class Project(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name=_("项目名称")
    )
    number = models.CharField(
        max_length=255, 
        unique=True, 
        verbose_name=_("项目编号")
    )
    funding_number = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name=_("经费编号")
    )
    leader = models.ForeignKey(
        Staff,
        related_name='led_projects',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("项目负责人")
    )
    start_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name=_("开始日期")
    )
    end_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name=_("结束日期")
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.APPROVED,
        verbose_name=_("项目状态")
    )
    category = models.ForeignKey(
        Category,
        related_name='category_projects',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("项目类别")
    )
    type = models.CharField(
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.OTHER,
        verbose_name=_("项目类型")
    )

    budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name=_("预算(万元)")
    )
    research_area = models.TextField(
        null=True, 
        blank=True,
        verbose_name=_("研究领域")
    )
    source = models.ForeignKey(
        Org,
        related_name='org_projects',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('项目来源单位')
    )
    undertake = models.CharField(
        max_length=20,
        choices=UndertakeType.choices,
        default=UndertakeType.HOST,
        verbose_name=_("承担方式")
    )
    remark = models.TextField(
        null=True, 
        blank=True,
        verbose_name=_("项目描述")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("创建时间")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("更新时间")
    )


    class Meta:
        verbose_name = _("项目")
        verbose_name_plural = _("项目")


    def __str__(self):
        return f"{self.title} ({self.number})"
    
    @property
    def status_display(self):
        """Return the display name for the project status"""
        return str(dict(ProjectStatus.choices).get(self.status, self.status))
        
    @property
    def undertake_display(self):
        """Return the display name for the project undertake type"""
        return str(dict(UndertakeType.choices).get(self.undertake, self.undertake))

    @property
    def type_display(self):
        """Return the display name for the project type"""
        return str(dict(ProjectType.choices).get(self.type, self.type))
