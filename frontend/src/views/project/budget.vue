<template>
  <div class="project-budget">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目预算管理</span>
          <el-button type="primary" @click="showDialog">新增预算</el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :model="filterForm" inline>
        <el-form-item label="项目编号">
          <el-input v-model="filterForm.project_number" placeholder="请输入项目编号" clearable />
        </el-form-item>
        <el-form-item label="预算名称">
          <el-input v-model="filterForm.name" placeholder="请输入预算名称" clearable />
        </el-form-item>
        <el-form-item label="预算类型">
          <el-select v-model="filterForm.type" placeholder="请选择预算类型" clearable>
            <el-option
              v-for="item in budgetTypeChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预算年度">
          <el-input v-model.number="filterForm.year" placeholder="请输入预算年度" clearable style="width: 100px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadBudgets">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 预算表格 -->
      <el-table :data="budgets" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="project_title" label="所属项目" min-width="200">
          <template #default="{ row }">
            <a href="javascript:void(0)" class="project-title-link" @click="showProjectDetail(row.project_id)">
              {{ row.project_title || getProjectTitle(row.project_id) }}
            </a>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="预算名称" min-width="150" />
        <el-table-column prop="amount" label="金额(万元)" width="120" align="right">
          <template #default="{ row }">
            {{ row.amount ? formatCurrency(row.amount) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="year" label="年度" width="100" />
        <el-table-column prop="type_display" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getBudgetTypeTagType(row.type)">{{ row.type_display || getBudgetTypeLabel(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editBudget(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteBudget(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total || 0"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadBudgets"
          @current-change="loadBudgets"
        />
      </div>
    </el-card>

    <!-- 预算表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="formTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="所属项目" prop="project_id">
          <el-select
            v-model="formData.project_id"
            placeholder="请选择所属项目"
            filterable
            clearable
          >
            <el-option
              v-for="project in projectOptions"
              :key="project.id"
              :label="project.title"
              :value="project.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="预算名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入预算名称" />
        </el-form-item>

        <el-form-item label="金额(万元)" prop="amount">
          <el-input v-model.number="formData.amount" :precision="2" placeholder="请输入金额" />
        </el-form-item>

        <el-form-item label="预算年度" prop="year">
          <el-input v-model.number="formData.year" placeholder="请输入预算年度" />
        </el-form-item>

        <el-form-item label="预算类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择预算类型">
            <el-option
              v-for="item in budgetTypeChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="备注">
          <el-input v-model="formData.remark" placeholder="请输入备注" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="projectDetailDialogVisible"
      title="项目详情"
      width="80%"
      :close-on-click-modal="false"
      fullscreen
    >
      <ProjectDetail :project-id="selectedProjectId" @close="handleProjectDetailClose" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox, ElDialog } from 'element-plus';
import { Project } from '@/api/project';
import { ProjectBudget, ProjectBudgetForm, ProjectBudgetFilter, Choice } from '@/api/projectBudget';
import { projectApi } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';
import ProjectDetail from './projectDetail.vue'; // 导入项目详情组件
// 由于找不到模块，暂时实现简单的 formatCurrency 和 formatDate 函数


// 格式化金额 - 修改为与 project.vue 中相同的实现
const formatCurrency = (value: number): string => {
  return value.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString();
};

// 预算列表数据
const budgets = ref<ProjectBudget[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const formRef = ref<any>(null);
const currentBudget = ref<ProjectBudget | null>(null);
const projectDetailDialogVisible = ref(false); // 项目详情对话框显示状态
const selectedProjectId = ref<number>(0); // 选中的项目ID

// 分页数据
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 筛选表单
const filterForm = reactive({
  project_id: undefined,
  project_number: '',
  name: '',
  type: undefined,
  year: undefined
});

// 表单数据
const formData = reactive<ProjectBudgetForm>({
  project_id: 0,
  name: '',
  amount: 0.00, // 修改为小数默认值
  year: new Date().getFullYear(),
  type: '',
  remark: ''
});

// 显示新增对话框
const showDialog = () => {
  currentBudget.value = null;
  // 重置表单数据
  formData.project_id = 0;
  formData.name = '';
  formData.amount = ''; // 修改为小数默认值
  formData.year = new Date().getFullYear();
  formData.type = '';
  formData.remark = '';
  dialogVisible.value = true;
};

// 表单规则
const formRules = {
  project_id: [
    { required: true, message: '请选择所属项目', trigger: 'change' }
  ],
  name: [
    { required: true, message: '请输入预算名称', trigger: 'blur' }
  ],
  // amount: [
  //   { required: true, message: '请输入金额', trigger: 'blur' },
  //   { type: 'number', min: 0.00, message: '金额必须大于等于0', trigger: 'blur' }
  // ],
  year: [
    { required: true, message: '请输入预算年度', trigger: 'blur' },
    { type: 'number', message: '请输入有效的年份', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择预算类型', trigger: 'change' }
  ]
};

// 下拉选项数据
const budgetTypeChoices = ref<Choice[]>([]);
const projectOptions = ref<{ id: number; title: string; }[]>([]);

// 表单标题计算属性
const formTitle = computed(() => {
  return currentBudget.value ? '编辑预算' : '新增预算';
});

// 加载预算列表
const loadBudgets = async () => {
  loading.value = true;
  try {
    // 构建筛选参数 - 只包含非空字段
    const params: ProjectBudgetFilter = {
      page: pagination.current,
      size: pagination.size
    };
    
    // 只添加非空的筛选字段
    Object.keys(filterForm).forEach(key => {
      const value = filterForm[key as keyof typeof filterForm];
      if (value !== undefined && value !== null && value !== '') {
        (params as any)[key] = value;
      }
    });

    const response = await projectBudgetApi.getProjectBudgets(params);
    budgets.value = response.items;
    pagination.total = response.total;
  } catch (error) {
    ElMessage.error('获取预算列表失败');
    console.error('获取预算列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 加载预算类型选项
const loadBudgetTypeChoices = async () => {
  try {
    budgetTypeChoices.value = await projectBudgetApi.getBudgetTypeChoices();
  } catch (error) {
    ElMessage.error('获取预算类型失败');
    console.error('获取预算类型失败:', error);
  }
};

// 加载项目选项
const loadProjectOptions = async () => {
  try {
    const projectsResponse = await projectApi.getProjects();
    projectOptions.value = projectsResponse.items.map(project => ({
      id: project.id,
      title: project.title
    }));
  } catch (error) {
    ElMessage.error('获取项目列表失败');
    console.error('获取项目列表失败:', error);
  }
};

// 重置筛选表单
const resetFilter = () => {
  Object.keys(filterForm).forEach(key => {
    filterForm[key as keyof typeof filterForm] = '' as any;
  });
  pagination.current = 1;
  loadBudgets();
};

// 编辑预算
const editBudget = (budget: ProjectBudget) => {
  currentBudget.value = budget;
  // 填充表单数据
  formData.project_id = budget.project_id;
  formData.name = budget.name;
  formData.amount = budget.amount || 0.00;
  formData.year = budget.year || new Date().getFullYear();
  formData.type = budget.type;
  formData.remark = budget.remark || '';
  dialogVisible.value = true;
};

// 删除预算
const deleteBudget = async (budget: ProjectBudget) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除预算项「${budget.name}」吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    await projectBudgetApi.deleteProjectBudget(budget.id);
    ElMessage.success('删除成功');
    loadBudgets();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除预算失败:', error);
    }
  }
};

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    if (currentBudget.value) {
      // 编辑模式
      await projectBudgetApi.updateProjectBudget(currentBudget.value.id, formData);
      ElMessage.success('更新成功');
    } else {
      // 新增模式
      await projectBudgetApi.createProjectBudget(formData);
      ElMessage.success('创建成功');
    }
    
    dialogVisible.value = false;
    loadBudgets();
  } catch (error) {
    ElMessage.error(currentBudget.value ? '更新失败' : '创建失败');
    console.error('提交表单失败:', error);
  }
};

// 显示项目详情
const showProjectDetail = (projectId: number) => {
  selectedProjectId.value = projectId;
  projectDetailDialogVisible.value = true;
};

// 处理项目详情对话框关闭事件
const handleProjectDetailClose = () => {
  projectDetailDialogVisible.value = false;
  loadBudgets(); // 刷新预算列表
};

// 获取预算类型标签样式
const getBudgetTypeTagType = (type: string): string => {
  const typeMap: Record<string, string> = {
    'INCOME': 'success',
    'EXPENSE': 'danger',
    'COORDINATION': 'primary',
    'OTHER': 'warning'
  };
  return typeMap[type] || 'info';
};

// 获取预算类型显示文本
const getBudgetTypeLabel = (type: string): string => {
  const typeChoice = budgetTypeChoices.value.find(choice => choice.value === type);
  return typeChoice ? typeChoice.label : type;
};

// 获取项目标题
const getProjectTitle = (projectId: number): string => {
  const project = projectOptions.value.find(p => p.id === projectId);
  return project ? project.title : `项目ID: ${projectId}`;
};

// 初始化数据
onMounted(() => {
  loadBudgets();
  loadBudgetTypeChoices();
  loadProjectOptions();
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.project-title-link {
  color: #409eff;
}

.project-title-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>