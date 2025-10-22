<template>
  <div class="container">
    <div class="header">
      <el-page-header
        :icon="Back"
        content="作者管理"
        @back="handleBack"
      />
      <div class="actions">
        <el-input
          v-model="searchForm.name"
          placeholder="请输入作者姓名"
          clearable
          class="search-input"
          @blur="handleSearch"
          @clear="handleSearch"
        />
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新增作者
        </el-button>
      </div>
    </div>

    <el-card class="content-card">
      <el-table
        v-loading="loading"
        :data="authorList"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="作者姓名" min-width="150" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="staff_name" label="关联员工" min-width="150">
          <template #default="scope">
            {{ scope.row.staff_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="external_organization" label="外部机构" min-width="200">
          <template #default="scope">
            {{ scope.row.external_organization || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(scope.row)"
              circle
            >
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(scope.row.id)"
              circle
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 作者编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="作者姓名" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="请输入作者姓名"
            clearable
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="formData.email"
            placeholder="请输入邮箱地址"
            type="email"
            clearable
          />
        </el-form-item>
        <el-form-item label="关联员工">
          <el-select
            v-model="formData.staff_id"
            placeholder="请选择关联员工"
            clearable
            filterable
          >
            <el-option
              v-for="staff in staffOptions"
              :key="staff.id"
              :label="staff.name"
              :value="staff.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="外部机构">
          <el-input
            v-model="formData.external_organization"
            placeholder="请输入外部机构名称（非本单位员工）"
            clearable
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Back, Plus, Edit, Delete } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import type { FormInstance } from 'element-plus';
import { achievementApi } from '@/api/achievement';
import { staffApi, StaffStatus } from '@/api/staff';
import type { Author, AuthorForm } from '@/api/achievement';

// 路由
const router = useRouter();

// 状态
const loading = ref(false);
const dialogVisible = ref(false);
const dialogTitle = ref('');
const formRef = ref<FormInstance>();

// 作者列表
const authorList = ref<Author[]>([]);

// 搜索表单
const searchForm = reactive({
  name: ''
});

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 员工选项
const staffOptions = ref<Array<{ id: number; name: string }>>([]);

// 表单数据
const formData = reactive<AuthorForm>({
  name: '',
  email: '',
  staff_id: undefined,
  external_organization: ''
});

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入作者姓名', trigger: 'blur' },
    { min: 1, max: 50, message: '作者姓名长度在1-50个字符之间', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
  ]
};

// 当前编辑的作者ID
let currentAuthorId: number | null = null;

/**
 * 加载员工选项列表
 * 用于作者编辑时关联内部员工
 */
const loadStaffOptions = async () => {
  try {
    // 调用员工API获取所有在职员工，设置较大的limit以获取完整列表
    const response = await staffApi.getStaffs(undefined, undefined, undefined, StaffStatus.ON_DUTY, 1, 1000);
    staffOptions.value = response.data.map(staff => ({ id: staff.id, name: staff.name }));
  } catch (error) {
    console.error('获取员工选项失败:', error);
    ElMessage.error('获取员工选项失败');
  }
};

/**
 * 加载作者列表
 * 支持搜索和分页
 */
const loadAuthors = async () => {
  loading.value = true;
  try {
    // 构建查询参数 - 只传递后端需要的参数
    const params: any = {
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize
    };
    
    // 应用搜索条件
    if (searchForm.name && searchForm.name.trim()) {
      // 确保搜索参数被正确设置
      params.filters = params.filters || {};
      params.filters.name = searchForm.name.trim();
    }

    console.log('请求参数:', params); // 添加日志记录完整请求参数
    const response = await achievementApi.getAuthors(params);
    
    // 由于后端API可能返回不同格式，这里做兼容处理
    if (Array.isArray(response)) {
      authorList.value = response;
      pagination.total = response.length;
    } else if (response.data && typeof response.total === 'number') {
      authorList.value = response.data;
      pagination.total = response.total;
    } else {
      // 直接使用响应作为数据（某些API可能直接返回数据数组）
      authorList.value = response;
      pagination.total = response.length || 0;
    }
  } catch (error) {
    console.error('获取作者列表失败:', error);
    ElMessage.error('获取作者列表失败');
  } finally {
    loading.value = false;
  }
};

/**
 * 重置表单数据
 */
const resetForm = () => {
  formRef.value?.resetFields();
  Object.assign(formData, {
    name: '',
    email: '',
    staff_id: undefined,
    external_organization: ''
  });
  currentAuthorId = null;
};

/**
 * 处理新增作者
 */
const handleCreate = () => {
  dialogTitle.value = '新增作者';
  resetForm();
  dialogVisible.value = true;
};

/**
 * 处理编辑作者
 * @param author 要编辑的作者对象
 */
const handleEdit = async (author: Author) => {
  dialogTitle.value = '编辑作者';
  currentAuthorId = author.id;
  
  // 填充表单数据
  Object.assign(formData, {
    name: author.name,
    email: author.email || '',
    staff_id: author.staff_id,
    external_organization: author.external_organization || ''
  });
  
  dialogVisible.value = true;
};

/**
 * 处理删除作者
 * @param id 作者ID
 */
const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个作者吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    await achievementApi.deleteAuthor(id);
    ElMessage.success('删除成功');
    // 重新加载列表
    await loadAuthors();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除作者失败:', error);
      ElMessage.error('删除失败，可能存在关联的论文');
    }
  }
};

/**
 * 处理表单提交
 * 根据是否有currentAuthorId决定是创建还是更新
 */
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    if (currentAuthorId) {
      // 更新作者
      await achievementApi.updateAuthor(currentAuthorId, formData);
      ElMessage.success('更新成功');
    } else {
      // 创建作者
      await achievementApi.createAuthor(formData);
      ElMessage.success('创建成功');
    }
    
    dialogVisible.value = false;
    // 重新加载列表
    await loadAuthors();
  } catch (error: any) {
    console.error('保存作者失败:', error);
    // 如果是API返回的错误信息，尝试提取显示
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail);
    } else {
      ElMessage.error(currentAuthorId ? '更新失败' : '创建失败');
    }
  }
};

/**
 * 处理搜索
 */
const handleSearch = () => {
  // 重置为第一页
  pagination.currentPage = 1;
  // 调用加载作者列表函数
  loadAuthors();
};

/**
 * 处理分页大小变化
 * @param size 新的每页数量
 */
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadAuthors();
};

/**
 * 处理当前页变化
 * @param current 新的当前页码
 */
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadAuthors();
};

/**
 * 处理返回
 */
const handleBack = () => {
  router.back();
};

// 初始化
onMounted(async () => {
  await loadStaffOptions();
  await loadAuthors();
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.search-input {
  width: 300px;
}

.content-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>