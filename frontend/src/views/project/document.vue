<template>
  <div class="app-container">
    <div class="search-form">
      <el-input
        v-model="searchForm.name"
        placeholder="文档名称"
        style="width: 200px;"
        clearable
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>

    <div class="toolbar">
      <el-button type="primary" @click="showDialog('create')">新增文档</el-button>
    </div>

    <el-table v-loading="loading" :data="documents.data" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="文档名称" />
      <el-table-column prop="file" label="文件路径" />
      <el-table-column prop="remark" label="备注" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="showDialog('edit', row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="documents.current_page"
        v-model:page-size="documents.size"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="documents.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 文档表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="80px">
        <el-form-item label="文档名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入文档名称" />
        </el-form-item>
        <el-form-item label="文件上传" prop="file">
          <el-upload
            ref="uploadRef"
            action=""
            :on-change="handleFileChange"
            :auto-upload="false"
            :show-file-list="true"
            accept="*"
          >
            <el-button type="primary">选择文件</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="formData.remark"
            type="textarea"
            placeholder="请输入备注信息"
            rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as documentApi from '@/api/document'
import type { ProjectDocumentIn, ProjectDocumentOut, ProjectDocumentFilter } from '@/api/document'
import type { ElForm } from 'element-plus'

// 从路由获取项目ID（这里假设从路由参数中获取，实际使用时需要根据项目路由配置调整）
const projectId = 1 // 临时值，实际应从路由获取

// 响应式数据
const loading = ref(false)
const documents = ref({
  data: [] as ProjectDocumentOut[],
  total: 0,
  current_page: 1,
  size: 10
})
const searchForm = reactive<ProjectDocumentFilter>({
  name: ''
})

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const dialogTitle = computed(() => dialogType.value === 'create' ? '新增文档' : '编辑文档')
const currentDocumentId = ref<number | null>(null)

// 表单相关
const formRef = ref<InstanceType<typeof ElForm>>()
const uploadRef = ref()
const formData = reactive<Partial<ProjectDocumentIn>>({
  name: '',
  file: null as File | null,
  remark: ''
})
const rules = reactive({
  name: [
    { required: true, message: '请输入文档名称', trigger: 'blur' },
    { min: 1, max: 100, message: '文档名称长度应在1到100个字符之间', trigger: 'blur' }
  ],
  file: [
    { required: true, message: '请选择文件', trigger: 'change' }
  ]
})

// 加载文档列表
const loadDocuments = async () => {
  loading.value = true
  try {
    const response = await documentApi.getProjectDocuments(projectId, {
      ...searchForm,
      page: documents.value.current_page,
      size: documents.value.size
    })
    documents.value = response
    loading.value = false
  } catch (error) {
    ElMessage.error('获取文档列表失败')
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  documents.value.current_page = 1
  loadDocuments()
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  documents.value.current_page = 1
  loadDocuments()
}

// 分页处理
const handleSizeChange = (size: number) => {
  documents.value.size = size
  loadDocuments()
}

const handleCurrentChange = (current: number) => {
  documents.value.current_page = current
  loadDocuments()
}

// 显示对话框
const showDialog = (type: 'create' | 'edit', row?: ProjectDocumentOut) => {
  dialogType.value = type
  dialogVisible.value = true
  
  // 重置表单
  formData.name = ''
  formData.file = null
  formData.remark = ''
  
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  
  if (type === 'edit' && row) {
    currentDocumentId.value = row.id
    // 填充表单数据
    formData.name = row.name
    formData.remark = row.remark || ''
  }
}

// 处理文件选择
const handleFileChange = (file: any) => {
  formData.file = file.raw
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 创建FormData对象用于文件上传
    const form = new FormData()
    form.append('name', formData.name)
    if (formData.file) {
      form.append('file', formData.file)
    }
    if (formData.remark) {
      form.append('remark', formData.remark)
    }
    
    if (dialogType.value === 'create') {
      await documentApi.createProjectDocument(projectId, formData)
      ElMessage.success('文档创建成功')
    } else {
      await documentApi.updateProjectDocument(projectId, currentDocumentId.value!, formData)
      ElMessage.success('文档更新成功')
    }
    
    dialogVisible.value = false
    loadDocuments()
  } catch (error) {
    ElMessage.error(dialogType.value === 'create' ? '文档创建失败' : '文档更新失败')
  }
}

// 删除文档
const handleDelete = async (id: number) => {
  try {
    await documentApi.deleteProjectDocument(projectId, id)
    ElMessage.success('文档删除成功')
    loadDocuments()
  } catch (error) {
    ElMessage.error('文档删除失败')
  }
}

// 初始加载
onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.toolbar {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}
</style>