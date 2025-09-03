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
    # 修改或添加type_name属性，确保与前端和schemas.py中的字段名一致
    def type_name(self):
        """Return the display name for the project type"""
        return str(dict(ProjectType.choices).get(self.type, self.type))


    #自定义 leader_name 字段
    @property
    def leader_name(self):
        return self.leader.name if self.leader else None
    
    #自定义 category_name 字段
    @property
    def category_name(self):
        return self.category.name if self.category else None
    
    #自定义 source_name 字段
    @property
    def source_name(self):
        return self.source.name if self.source else None



### 项目预算
# from django.db import models

from enum import Enum

class ProjectBudgetType(Enum):
    INCOME = "收入"
    EXPENSE = "支出"
    COORDINATION = "统筹"
    OTHER = "其他"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ProjectBudget(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(
        Project, 
        related_name='budgets',
        on_delete=models.CASCADE  # Django需要指定外键删除行为，这里使用CASCADE作为默认
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True,
        help_text="金额(万元)"  # Django中使用help_text替代description
    )
    year = models.IntegerField(null=True)
    type = models.CharField(
        max_length=20,
        choices=ProjectBudgetType.choices(),
        default=ProjectBudgetType.INCOME.value
    )
    remark = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 可以在这里添加元数据，如数据库表名等
        # db_table = 'project_budget'
        pass