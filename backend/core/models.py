from django.db import models

class Org(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=255, null=True, blank=True, help_text="组织邮箱")
    org_type = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "orgs"


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='departments', help_text="所属组织")
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "departments"


class Category(models.Model):
    """类别模型"""
    name = models.CharField(max_length=50, help_text="类别名称")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL, help_text="父类别")
    weight = models.IntegerField(default=0, help_text="权重")
    sort_order = models.IntegerField(default=0, help_text="排序")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        unique_together = ('name', 'parent')
