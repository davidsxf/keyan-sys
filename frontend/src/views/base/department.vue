<template>
  <div class="department-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>部门管理</h2>
          <el-button type="primary" @click="showCreateDialog(null)">
            新增部门
          </el-button>
        </div>
      </template>

      <!-- 部门树形表格 -->
      <el-table
        :data="departments"
        row-key="id"
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="部门名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="240">
          <template #default="{ row }">
            <el-button size="small" @click="showCreateDialog(row)">
              添加子部门
            </el-button>
            <el-button size="small" @click="editDepartment(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteDepartment(row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

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
          label-width="80px"
        >
          <el-form-item label="部门名称" prop="name">
            <el-input v-model="form.name" />
          </el-form-item>
          <el-form-item label="父部门" v-if="!isEditing">
            <el-select v-model="form.parent_id" clearable placeholder="可选">
              <el-option
                v-for="dept in flatDepartments"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
                :disabled="dept.id === editingId"
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
        </el-form>
        
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确认</el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { departmentApi } from '@/api/department'
import type { Department, DepartmentForm } from '@/api/department'

// 数据状态
const departments = ref<Department[]>([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number>()
const parentDepartment = ref<Department | null>(null)

// 表单引用和验证规则
const formRef = ref<FormInstance>()
const form = reactive<DepartmentForm>({
  name: '',
  description: '',
  parent_id: null
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入部门名称', trigger: 'blur' },
    { min: 2, max: 255, message: '长度在 2 到 255 个字符', trigger: 'blur' }
  ]
}

// 计算属性
const dialogTitle = computed(() => {
  if (isEditing.value) return '编辑部门'
  return parentDepartment.value ? `为【${parentDepartment.value.name}】添加子部门` : '新增部门'
})

// 扁平化的部门列表（用于父部门选择）
const flatDepartments = computed(() => {
  const flatten: Department[] = []
  
  function flattenDepartments(depts: Department[]) {
    depts.forEach(dept => {
      flatten.push({ ...dept, children: undefined })
      if (dept.children && dept.children.length > 0) {
        flattenDepartments(dept.children)
      }
    })
  }
  
  flattenDepartments(departments.value)
  return flatten
})

// 方法
const loadDepartments = async () => {
  try {
    departments.value = await departmentApi.getDepartments()
  } catch (error) {
    ElMessage.error('获取部门列表失败')
  }
}

const showCreateDialog = (parent: Department | null) => {
  isEditing.value = false
  editingId.value = undefined
  parentDepartment.value = parent
  
  Object.assign(form, {
    name: '',
    description: '',
    parent_id: parent ? parent.id : null
  })
  
  dialogVisible.value = true
}

const editDepartment = (department: Department) => {
  isEditing.value = true
  editingId.value = department.id
  parentDepartment.value = null
  
  Object.assign(form, {
    name: department.name,
    description: department.description || '',
    parent_id: department.parent_id || null
  })
  
  dialogVisible.value = true
}

const submitForm = async () => {
  try {
    if (!formRef.value) return
    const valid = await formRef.value.validate()
    if (!valid) return
    
    if (isEditing.value && editingId.value) {
      await departmentApi.updateDepartment(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await departmentApi.createDepartment(form)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    loadDepartments()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

const deleteDepartment = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确认删除该部门？此操作会同时删除其所有子部门。',
      '警告',
      { type: 'warning' }
    )
    
    await departmentApi.deleteDepartment(id)
    ElMessage.success('删除成功')
    loadDepartments()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 生命周期
onMounted(() => {
  loadDepartments()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 确保操作列有足够宽度 */
.el-table .el-table__column--operation {
  width: 240px !important;
}


</style>
