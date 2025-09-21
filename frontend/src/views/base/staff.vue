<template>
  <div class="staff-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>员工管理</h2>
          <el-button type="primary" @click="showCreateDialog">
            新增员工
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选栏 -->
      <div class="filter-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名、邮箱、电话或职位"
          style="width: 300px"
          @keyup.enter="loadStaffs"
        >
          <template #append>
            <el-button @click="loadStaffs">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>

        <el-select
          v-model="selectedDepartment"
          placeholder="按部门筛选"
          clearable
          style="width: 200px; margin-left: 10px"
          @change="loadStaffs"
        >
          <el-option
            v-for="dept in departments"
            :key="dept.id"
            :label="dept.name"
            :value="dept.id"
          />
        </el-select>

        <el-select
          v-model="selectedTeam"
          placeholder="按团队筛选"
          clearable
          style="width: 200px; margin-left: 10px"
          @change="loadStaffs"
        >
          <el-option
            v-for="team in teams"
            :key="team.id"
            :label="team.name"
            :value="team.id"
          />
        </el-select>

        <el-select
          v-model="selectedStatus"
          placeholder="按状态筛选"
          clearable
          style="width: 200px; margin-left: 10px"
          @change="loadStaffs"
        >
          <el-option
            v-for="status in statusOptions"
            :key="status.value"
            :label="status.label"
            :value="status.value"
          />
        </el-select>
      </div>

      <!-- 员工表格 -->
      <el-table :data="staffs" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="birthday" label="生日" width="120">
          <template #default="{ row }">
            {{ formatDate(row.birthday) }}
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="department_name" label="部门" />
        <el-table-column prop="team_name" label="团队" />
        <el-table-column prop="position" label="职位" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_team_leader" label="团队领导" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_team_leader" type="success">是</el-tag>
            <span v-else>否</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="editStaff(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteStaff(row.id)">
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
          @size-change="loadStaffs"
          @current-change="loadStaffs"
        />
      </div>
    </el-card>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="生日">
          <el-date-picker
            v-model="form.birthday"
            type="date"
            placeholder="选择生日"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        
        <el-form-item label="入职日期">
          <el-date-picker
            v-model="form.entry_date"
            type="date"
            placeholder="选择入职日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="部门">
          <el-select v-model="form.department_id" clearable placeholder="请选择">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="团队">
          <el-select v-model="form.team_id" clearable placeholder="请选择">
            <el-option
              v-for="team in teams"
              :key="team.id"
              :label="team.name"
              :value="team.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="职位">
          <el-input v-model="form.position" />
        </el-form-item>
        
        <el-form-item label="团队领导">
          <el-checkbox v-model="form.is_team_leader">是否为团队领导</el-checkbox>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option
              v-for="status in statusOptions"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="form.remark"
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
import { staffApi, departmentApi, teamApi, StaffStatus } from '@/api/staff'
import type { Staff, StaffForm, DepartmentOption, TeamOption } from '@/api/staff'

// 数据状态
const staffs = ref<Staff[]>([])
const departments = ref<DepartmentOption[]>([])
const teams = ref<TeamOption[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const selectedDepartment = ref<number>()
const selectedTeam = ref<number>()
const selectedStatus = ref<StaffStatus>()
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

// 对话框状态
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number>()

// 表单引用和验证规则
const formRef = ref<FormInstance>()
const form = reactive<StaffForm>({
  name: '',
  gender: '男',
  birthday: undefined,
  email: undefined,
  entry_date: undefined,
  department_id: null,
  team_id: null,
  position: '',
  is_team_leader: false,
  status: StaffStatus.ON_DUTY,
  phone: '',
  remark: ''
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入员工姓名', trigger: 'blur' },
    { min: 2, max: 255, message: '长度在 2 到 255 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
})

// 状态选项
const statusOptions = [
  { value: StaffStatus.ON_DUTY, label: '在职' },
  { value: StaffStatus.OFF_DUTY, label: '离职' },
  { value: StaffStatus.RETIRE, label: '退休' }
]

// 计算属性
const dialogTitle = computed(() => isEditing.value ? '编辑员工' : '新增员工')

// 方法
const loadStaffs = async () => {
  try {
    loading.value = true
    const result = await staffApi.getStaffs(
      searchKeyword.value,
      selectedDepartment.value,
      selectedTeam.value,
      selectedStatus.value,
      currentPage.value,
      pageSize.value
    )
    staffs.value = result.data
    totalCount.value = result.total // 设置总条数
  } catch (error) {
    ElMessage.error('获取员工列表失败')
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    departments.value = await departmentApi.getDepartmentOptions()
  } catch (error) {
    ElMessage.error('获取部门列表失败')
  }
}

const loadTeams = async () => {
  try {
    teams.value = await teamApi.getTeamOptions()
  } catch (error) {
    ElMessage.error('获取团队列表失败')
  }
}

const showCreateDialog = () => {
  isEditing.value = false
  editingId.value = undefined
  Object.assign(form, {
    name: '',
    gender: '男',
    birthday: undefined,
    email: undefined,
    entry_date: undefined,
    department_id: null,
    team_id: null,
    position: '',
    is_team_leader: false,
    status: StaffStatus.ON_DUTY,
    phone: '',
    remark: ''
  })
  dialogVisible.value = true
}

const editStaff = (staff: Staff) => {
  isEditing.value = true
  editingId.value = staff.id
  Object.assign(form, {
    name: staff.name,
    gender: staff.gender || '男',
    birthday: staff.birthday || undefined,
    email: staff.email || undefined,
    entry_date: staff.entry_date || undefined,
    department_id: staff.department_id || null,
    team_id: staff.team_id || null,
    position: staff.position || '',
    is_team_leader: staff.is_team_leader,
    status: convertStatusToEnum(staff.status),
    phone: staff.phone || '',
    remark: staff.remark || ''
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
      // 更新员工
      await staffApi.updateStaff(editingId.value, form)
      ElNotification.success({
        title: '成功',
        message: '员工更新成功'
      })
      dialogVisible.value = false
      loadStaffs()
    } else {
      // 创建员工
      await staffApi.createStaff(form)
      ElNotification.success({
        title: '成功',
        message: '员工创建成功'
      })
      dialogVisible.value = false
      loadStaffs()
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

const deleteStaff = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个员工吗？此操作不可恢复。',
      '警告',
      { type: 'warning' }
    )
    
    await staffApi.deleteStaff(id)
    ElNotification.success({
      title: '成功',
      message: '员工已删除'
    })
    loadStaffs()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const getStatusTagType = (status: string) => {
  switch (status) {
    case StaffStatus.ON_DUTY: return 'success'
    case StaffStatus.OFF_DUTY: return 'danger'
    case StaffStatus.RETIRE: return 'info'
    default: return ''
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

// 将字符串状态转换为枚举类型
const convertStatusToEnum = (status: string): StaffStatus => {
  switch (status) {
    case '在职': return StaffStatus.ON_DUTY
    case '离职': return StaffStatus.OFF_DUTY
    case '退休': return StaffStatus.RETIRE
    default: return StaffStatus.ON_DUTY
  }
}

// 生命周期
onMounted(() => {
  loadStaffs()
  loadDepartments()
  loadTeams()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
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
