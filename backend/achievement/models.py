from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Staff

# Create your models here.
class Author(models.Model):
    """作者信息模型（扩展版）"""
    name = models.CharField(_("姓名"), max_length=100)
    email = models.EmailField(_("邮箱"), blank=True, null=True)
    # 关联单位员工，可为空（表示外单位作者）
    staff = models.OneToOneField(
        Staff, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="author_profile",
        verbose_name=_("关联员工")
    )
    # 外单位作者的单位信息
    external_organization = models.CharField(_("外单位名称"), max_length=200, blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("作者")
        verbose_name_plural = _("作者")

class Journal(models.Model):
    """期刊信息模型"""
    name = models.CharField(_("刊名"), max_length=200)
    issn = models.CharField(_("ISSN"), max_length=20, unique=True)
    jcr_quartile = models.CharField(_("JCR分区"), max_length=10, blank=True)
    impact_factor = models.FloatField(_("影响因子"), blank=True, null=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("期刊")
        verbose_name_plural = _("期刊")

class Paper(models.Model):
    """论文信息模型"""
    title = models.CharField(_("篇名"), max_length=500)
    first_authors = models.ManyToManyField(
        Author, 
        related_name="first_author_papers",
        verbose_name=_("第一作者/共一作者")
    )
    corresponding_authors = models.ManyToManyField(
        Author, 
        related_name="corresponding_author_papers",
        verbose_name=_("通讯作者/共同通讯作者")
    )
    journal = models.ForeignKey(
        Journal, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="papers",
        verbose_name=_("期刊")
    )
    publication_year = models.IntegerField(_("发表年份"))
    unit_ranking = models.IntegerField(_("单位排名"))
    page_numbers = models.CharField(_("页码范围"), max_length=50, blank=True)
    keywords = models.CharField(_("关键词"), max_length=500, blank=True)
    abstract = models.TextField(_("摘要"), blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("论文")
        verbose_name_plural = _("论文")
        ordering = ["-publication_year"]
