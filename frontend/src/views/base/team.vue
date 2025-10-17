<template>
  <div class="team-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>团队管理</h2>
          <el-button type="primary" @click="showCreateDialog">
            新增团队
          </el-button>
        </div>
      </template>


      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索团队名称、描述或研究领域"
          style="width: 300px"
          @keyup.enter="loadTeams"
        >
          <template #append>
            <el-button @click="loadTeams">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        
        <el-select
          v-model="selectedDepartment"
          placeholder="按部门筛选"
          clearable
          style="width: 200px; margin-left: 10px"
          @change="loadTeams"
        >
          <el-option
            v-for="dept in departments"
            :key="dept.id"
            :label="dept.name"
            :value="dept.id"
          />
        </el-select>
      </div>


      <!-- 团队表格 -->
      <el-table :data="teams" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="团队名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="research_field" label="研究领域" />
        <el-table-column prop="department_name" label="所属部门" />
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="editTeam(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTeam(row.id)">
              删除
            </el-button>
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
          @size-change="loadTeams"
          @current-change="loadTeams"
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
        <el-form-item label="团队名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属部门">
          <el-select v-model="form.department_id" clearable placeholder="请选择">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="研究领域">
          <el-input v-model="form.research_field" placeholder="请输入团队主要研究领域" />
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
import { teamApi, departmentApi } from '@/api/team'
import type { Team, TeamForm, DepartmentOption } from '@/api/team'


// 数据状态
const teams = ref<Team[]>([])
const departments = ref<DepartmentOption[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const selectedDepartment = ref<number>()
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)


// 对话框状态
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number>()


// 表单引用和验证规则
const formRef = ref<FormInstance>()
const form = reactive<TeamForm>({
  name: '',
  description: '',
  research_field: '',
  department_id: null
})


const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入团队名称', trigger: 'blur' },
    { min: 2, max: 255, message: '长度在 2 到 255 个字符', trigger: 'blur' }
  ]
})


// 计算属性
const dialogTitle = computed(() => isEditing.value ? '编辑团队' : '新增团队')


// 方法
const loadTeams = async () => {
  try {
    loading.value = true
    const result = await teamApi.getTeams(
      searchKeyword.value, 
      selectedDepartment.value, 
      currentPage.value, 
      pageSize.value
    )
    teams.value = result.data
    totalCount.value = result.total // 设置总条数
  } catch (error) {
    ElMessage.error('获取团队列表失败')
  } finally {
    loading.value = false
  }
}


const loadDepartments = async () => {
  try {
    departments.value = await departmentApi.getDepartmentOptions()
  } catch (error) {
    ElMessage.error('获取部门选项失败')
  }
}


const showCreateDialog = () => {
  isEditing.value = false
  editingId.value = undefined
  Object.assign(form, {
    name: '',
    description: '',
    research_field: '',
    department_id: null
  })
  dialogVisible.value = true
}


const editTeam = (team: Team) => {
  isEditing.value = true
  editingId.value = team.id
  Object.assign(form, {
    name: team.name,
    description: team.description || '',
    research_field: team.research_field || '',
    department_id: team.department_id || null
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
      // 更新团队
      await teamApi.updateTeam(editingId.value, form)
      ElNotification.success({
        title: '成功',
        message: '团队更新成功'
      })
      dialogVisible.value = false
      loadTeams()
    } else {
      // 创建团队
      await teamApi.createTeam(form)
      ElNotification.success({
        title: '成功',
        message: '团队创建成功'
      })
      dialogVisible.value = false
      loadTeams()
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}


const deleteTeam = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个团队吗？此操作不可恢复。',
      '警告',
      { type: 'warning' }
    )
    
    await teamApi.deleteTeam(id)
    ElNotification.success({
      title: '成功',
      message: '团队已删除'
    })
    loadTeams()
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
  loadTeams()
  loadDepartments()
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
  display: flex;
  align-items: center;
}


.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
