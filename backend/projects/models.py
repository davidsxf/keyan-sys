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

#     participants = models.ManyToManyField(
#     Staff,
#     through='ProjectStaff',
#     related_name='participated_projects',
#     verbose_name=_("参与人员"),
#     blank=True
# )
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
from django.db import models
from django.utils.translation import gettext_lazy as _


# 修复前
# 将普通Enum改为Django的TextChoices，与项目中其他枚举类型保持一致
# def ProjectBudgetType(models.TextChoices):
#     INCOME = "INCOME", _("收入")
#     EXPENSE = "EXPENSE", _("支出")
#     COORDINATION = "COORDINATION", _("统筹")
#     OTHER = "OTHER", _("其他")

# 修复后
class ProjectBudgetType(models.TextChoices):
    INCOME = "INCOME", _("收入")
    EXPENSE = "EXPENSE", _("支出")
    COORDINATION = "COORDINATION", _("统筹")
    OTHER = "OTHER", _("其他")

class ProjectBudget(models.Model):
    # 移除手动定义的id字段，Django会自动创建自增主键
    project = models.ForeignKey(
        Project, 
        related_name='budgets',
        on_delete=models.CASCADE,  # 明确指定级联删除行为
        verbose_name=_('所属项目')  # 添加verbose_name提高可读性
    )
    name = models.CharField(
        max_length=255, 
        verbose_name=_('预算名称'),
        help_text=_('预算项的具体名称')
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,  # 允许表单提交空值
        verbose_name=_('金额(万元)'),
        help_text=_('预算金额，单位为万元')
    )
    year = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name=_('年度'),
        help_text=_('预算所属的年份')
    )
    type = models.CharField(
        max_length=20,
        choices=ProjectBudgetType.choices,  # 直接使用choices属性
        default=ProjectBudgetType.INCOME,  # 使用枚举成员而非.value
        verbose_name=_('类型'),
        help_text=_('预算类型：收入、支出、统筹或其他')
    )
    remark = models.TextField(
        null=True, 
        blank=True,
        verbose_name=_('备注'),
        help_text=_('关于预算项的补充说明')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('更新时间')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('创建时间')
    )

    class Meta:
        verbose_name = _('项目预算')
        verbose_name_plural = _('项目预算')
        ordering = ['-created_at']  # 默认按创建时间降序排列
        # 可选：添加数据库表名
        # db_table = 'project_budget'

    def __str__(self):
        return f'{self.project.title} - {self.name} ({self.get_type_display()})'





# 项目参与人员


class ProjectStaff(models.Model):
    ROLE_CHOICES = [
        # ('leader', '负责人'),
        ('member', '成员'),
        ('advisor', '顾问'),
    ]
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_("项目")
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name=_("参与人员")
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name=_("角色")
    )
    order = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("排序")
    )
    join_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("加入时间")
    )
    leave_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("离开日期")
    )
    remark = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("备注")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('project', 'staff')]  # 同一项目同一人只记录一次
        verbose_name = _("项目参与人员")
        verbose_name_plural = _("项目参与人员")

    def __str__(self):
        return f"{self.staff.name} - {self.project.title} ({self.role})"


    @property
    def project_title(self):
        return self.project.title if self.project else None

    @property
    def staff_name(self):
        return self.staff.name if self.staff else None

    @property
    def staff_department(self):
        return self.staff.department.name if self.staff and self.staff.department else None

    @property
    def role_display(self):
        return str(dict(ProjectStaff.ROLE_CHOICES).get(self.role, self.role))



#项目文档
class ProjectDocument(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_("项目")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("文档名称")
    )
    file = models.FileField(
        upload_to='project_documents/',
        verbose_name=_("文档文件")
    )
    remark = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("备注")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("项目文档")
        verbose_name_plural = _("项目文档")

    def __str__(self):
        return f"{self.name} - {self.project.title}"