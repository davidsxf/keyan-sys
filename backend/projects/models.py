from django.db import models
from core.models import Category, Org
from users.models import Staff

from django.utils.translation import gettext_lazy as _




# 项目状态选项
class ProjectStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", _("在研")
    COMPLETED = "COMPLETED", _("结题")
    TERMINATED = "TERMINATED", _("终止")



#项目级别 ：国家级 省部级 基本科研业务费 地方其他项目 其他

class ProjectLevel(models.TextChoices):
    NATIONAL = "NATIONAL", _("国家级")
    PROVINCIAL = "PROVINCIAL", _("省部级")
    BASIC_RESEARCH = "BASIC_RESEARCH", _("基本科研业务费")
    LOCAL_OTHER = "LOCAL_OTHER", _("地方其他项目")
    OTHER = "OTHER", _("其他")




# 承担方式选择
class UndertakeType(models.TextChoices):
    HOST = "HOST", _("主持")
    PARTICIPATE = "PARTICIPATE", _("参加")





# 项目类型选项（如果不使用外键关联Category模型，可直接使用此选项）

class ProjectType(models.TextChoices):
    NATIONAL_MAJOR_SCI_TECH = "NATIONAL_MAJOR_SCI_TECH", _("国家科技重大专项")
    NATIONAL_BIO_BREEDING = "NATIONAL_BIO_BREEDING", _("国家生物育种专项")
    NATIONAL_KEY_RD = "NATIONAL_KEY_RD", _("国家重点研发计划")
    NATIONAL_NATURAL_SCI_FUND = "NATIONAL_NATURAL_SCI_FUND", _("国家自然科学基金")
    SCI_TECH_INFRA_PLATFORM = "SCI_TECH_INFRA_PLATFORM", _("科技基础条件平台专项")
    SCI_TECH_BASIC_WORK = "SCI_TECH_BASIC_WORK", _("科技基础性工作专项")
    MODERN_AGRI_IND_TECH_SYSTEM = "MODERN_AGRI_IND_TECH_SYSTEM", _("现代农业产业技术体系")
    SELF_FULFILLMENT = "SELF_FULFILLMENT", _("自有履职专项")
    NATIONAL_MINISTERIAL_OTHER = "NATIONAL_MINISTERIAL_OTHER", _("国家和部级其它项")
    STANDARD_REVISION_NATIONAL = "STANDARD_REVISION_NATIONAL", _("标准制修订项目（国标）")
    STANDARD_REVISION_INDUSTRY = "STANDARD_REVISION_INDUSTRY", _("标准制修订项目（行标）")
    STANDARD_REVISION_LOCAL = "STANDARD_REVISION_LOCAL", _("标准制修订项目（地标）")
    INTERNATIONAL_COOPERATION = "INTERNATIONAL_COOPERATION", _("国际合作项目")
    BASIC_RESEARCH_FUND = "BASIC_RESEARCH_FUND", _("基本科研业务费专项")
    PROVINCIAL_PLAN = "PROVINCIAL_PLAN", _("省级计划项目")
    LOCAL_OTHER_PROJECT = "LOCAL_OTHER_PROJECT", _("地方其它项目")
    OTHER_PROJECT_PLAN = "OTHER_PROJECT_PLAN", _("其它项目计划")





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
        default=ProjectStatus.IN_PROGRESS,
        verbose_name=_("项目状态")
    )
    level = models.CharField(
        max_length=20,
        choices=ProjectLevel.choices,
        default=ProjectLevel.NATIONAL,
        verbose_name=_("项目级别")
    )
    type = models.CharField(
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.LOCAL_OTHER_PROJECT,
        verbose_name=_("项目类型")
    )
    category = models.ForeignKey(
        Category,
        related_name='category_projects',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("项目类别")
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
        return f"{self.title}"

    @property
    def level_display(self):
        """Return the display name for the project level"""
        return str(dict(ProjectLevel.choices).get(self.level, self.level))
    
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


### 项目负责人变更
class ProjectLeaderChange(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='leader_changes',
        on_delete=models.CASCADE,
        verbose_name=_('所属项目')
    )
    leader = models.ForeignKey(
        Staff,
        related_name='led_project_leader_changes',
        on_delete=models.CASCADE,
        verbose_name=_('新负责人')
    )
    change_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('变更日期')
    )
    remark = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('变更备注')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('更新时间')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('创建时间')
    )

### 项目预算
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# 修复前
# 将普通Enum改为Django的TextChoices，与项目中其他枚举类型保持一致
# def ProjectBudgetType(models.TextChoices):
#     INCOME = "INCOME", _("收入")
#     EXPENSE = "EXPENSE", _("支出")
#     COORDINATION = "COORDINATION", _("统筹")
#     OTHER = "OTHER", _("其他")

# 修复后
class ProjectBudgetType(models.TextChoices):
    INCOME = "INCOME", _("到账经费")
    EXPENSE = "EXPENSE", _("外拨经费")
    # COORDINATION = "COORDINATION", _("统筹")
    # OTHER = "OTHER", _("其他")

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