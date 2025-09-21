<template>
  <div class="org-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>组织管理</h2>
          <el-button type="primary" @click="showCreateDialog">新增组织</el-button>
        </div>
      </template>


      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索组织名称、描述或类型"
          style="width: 300px"
          @keyup.enter="loadOrgs"
        >
          <template #append>
            <el-button @click="loadOrgs">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>


      <!-- 组织表格 -->
      <el-table :data="orgs" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="组织名称" />
        <el-table-column prop="org_type" label="类型" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="editOrg(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteOrg(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>


      <!-- 分页控件 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalCount"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadOrgs"
          @current-change="loadOrgs"
        />
      </div>
    </el-card>


    <!-- 创建/编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="组织名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="组织类型" prop="org_type">
          <el-input v-model="form.org_type" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>


<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, ElNotification, type FormInstance, type FormRules } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { orgApi } from '@/api/org'
import type { Org, OrgForm } from '@/api/org'


// 数据状态
const orgs = ref<Org[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)


// 对话框状态
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number>()


// 表单引用和验证规则
const formRef = ref<FormInstance>()
const form = reactive<OrgForm>({
  name: '',
  description: '',
  phone: '',
  email: '',
  org_type: ''
})



const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入组织名称', trigger: 'blur' },
    { min: 2, max: 255, message: '长度在 2 到 255 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
})


// 计算属性
const dialogTitle = computed(() => isEditing.value ? '编辑组织' : '新增组织')


// 方法
const loadOrgs = async () => {
  try {
    loading.value = true
    const result = await orgApi.getOrgs(searchKeyword.value, currentPage.value, pageSize.value)
    orgs.value = result.data
    totalCount.value = result.total // 设置总条数
  } catch (error) {
    ElMessage.error('获取组织列表失败')
  } finally {
    loading.value = false
  }
}


const showCreateDialog = () => {
  isEditing.value = false
  editingId.value = undefined
  Object.assign(form, {
    name: '',
    description: '',
    phone: '',
    email: '',
    org_type: ''
  })
  dialogVisible.value = true
}


const editOrg = (org: Org) => {
  isEditing.value = true
  editingId.value = org.id
  Object.assign(form, {
    name: org.name,
    description: org.description || '',
    phone: org.phone || '',
    email: org.email || '',
    org_type: org.org_type || ''
  })
  dialogVisible.value = true
}


const submitForm = async () => {
  try {
    // 表单验证
    if (!formRef.value) return
    const valid = await formRef.value.validate()
    if (!valid) return
    
    if (isEditing.value && editingId.value) {
      // 更新组织
      await orgApi.updateOrg(editingId.value, form)
      ElNotification.success({
        title: '成功',
        message: '组织更新成功'
      })
      dialogVisible.value = false
      loadOrgs()
    } else {
      // 创建组织
      await orgApi.createOrg(form)
      ElNotification.success({
        title: '成功',
        message: '组织创建成功'
      })
      dialogVisible.value = false
      loadOrgs()
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}


const deleteOrg = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个组织吗？此操作不可恢复。',
      '警告',
      { type: 'warning' }
    )
    
    await orgApi.deleteOrg(id)
    ElNotification.success({
      title: '成功',
      message: '组织已删除'
    })
    loadOrgs()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}





const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}


// 生命周期
onMounted(() => {
  loadOrgs()
})
</script>


<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.search-bar {
  margin-bottom: 20px;
}


.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>