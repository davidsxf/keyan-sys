<template>
  <div class="project-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目详情</span>
          <el-button-group>
            <el-button type="primary" @click="handleEdit">编辑</el-button>
            <el-button @click="handleBack">返回</el-button>
          </el-button-group>
        </div>
      </template>

      <div class="detail-container">
        <!-- 项目基本信息 -->
        <el-card class="info-card" title="基本信息">
          <el-descriptions column="1" :border="true">
            <el-descriptions-item label="项目名称">{{ project.title }}</el-descriptions-item>
            <el-descriptions-item label="项目编号">{{ project.number }}</el-descriptions-item>
            <el-descriptions-item label="课题编号">{{ project.funding_number || '-' }}</el-descriptions-item>
            <el-descriptions-item label="项目负责人">{{ project.leader_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="项目状态"><el-tag>{{ project.status_display }}</el-tag></el-descriptions-item>
            <el-descriptions-item label="项目类别">{{ project.category_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="项目类型">{{ project.type_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="研究领域">{{ project.research_area || '-' }}</el-descriptions-item>
            <el-descriptions-item label="立项时间">{{ formatDate(project.start_date) }}</el-descriptions-item>
            <el-descriptions-item label="结项时间">{{ formatDate(project.end_date) }}</el-descriptions-item>
            <el-descriptions-item label="承担单位">{{ project.undertake_display }}</el-descriptions-item>
            <el-descriptions-item label="项目来源">{{ project.source_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="项目预算(万元)">{{ project.budget ? project.budget.toFixed(2) : '0.00' }}</el-descriptions-item>
            <el-descriptions-item label="备注">{{ project.remark || '-' }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDateTime(project.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ formatDateTime(project.updated_at) }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 项目经费信息 -->
        <el-card class="budget-card" title="经费信息" v-loading="budgetDataLoading">
          <div class="budget-header">
            <el-button type="primary" size="small" @click="showBudgetDialog">新增预算</el-button>
          </div>

          <!-- 预算统计 -->
          <div class="budget-summary">
            <el-row :gutter="20">
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">总预算</div>
                  <div class="stat-value">{{ project.budget ? project.budget.toFixed(2) : '0.00' }}万元</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">收入</div>
                  <div class="stat-value income">{{ incomeBudget.toFixed(2) }}万元</div>
                </div>
              </el-col>
            
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">支出</div>
                  <div class="stat-value expense">{{ expenseBudget.toFixed(2) }}万元</div>
                </div>
              </el-col>
                <!-- 统筹 -->
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">统筹</div>
                  <div class="stat-value other">{{ otherBudget.toFixed(2) }}万元</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">其他</div>
                  <div class="stat-value other">{{ otherBudget.toFixed(2) }}万元</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="stat-item">
                  <div class="stat-label">结余</div>
                  <div class="stat-value other">{{ remainingBudget.toFixed(2) }}万元</div>
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 预算表格 -->
          <el-table :data="budgets" style="margin-top: 20px">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="预算名称" min-width="150" />
            <el-table-column prop="amount" label="金额(万元)" width="120" align="right">
              <template #default="{ row }">
                {{ row.amount ? row.amount.toFixed(2) : '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="year" label="年度" width="100" />
            <el-table-column prop="type_display" label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="getBudgetTypeTagType(row.type)">{{ row.type_display || getBudgetTypeLabel(row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" min-width="150" />
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editBudget(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteBudget(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-card>

    <!-- 预算表单对话框 -->
    <el-dialog
      v-model="budgetDialogVisible"
      :title="budgetFormTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="budgetFormRef"
        :model="budgetFormData"
        :rules="budgetFormRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="预算名称" prop="name">
          <el-input v-model="budgetFormData.name" placeholder="请输入预算名称" />
        </el-form-item>
        <el-form-item label="金额(万元)" prop="amount">
          <el-input v-model.number="budgetFormData.amount" placeholder="请输入金额" />
        </el-form-item>
        <el-form-item label="预算年度" prop="year">
          <el-input v-model.number="budgetFormData.year" placeholder="请输入预算年度" />
        </el-form-item>
        <el-form-item label="预算类型" prop="type">
          <el-select v-model="budgetFormData.type" placeholder="请选择预算类型">
            <el-option
              v-for="item in budgetTypeChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="budgetFormData.remark" type="textarea" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="budgetDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitBudgetForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Project } from '@/api/project';
import { ProjectBudget, ProjectBudgetForm, Choice } from '@/api/projectBudget';
import { projectApi } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';

// 定义props和emit
const props = defineProps<{
  projectId: number;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

// 项目数据
const project = ref<Project>({} as Project);
const projectLoading = ref(true);

// 预算数据
const budgets = ref<ProjectBudget[]>([]);
const budgetDataLoading = ref(false);
const budgetTypeChoices = ref<Choice[]>([]);
const budgetDialogVisible = ref(false);
const budgetFormRef = ref<any>(null);
const currentBudget = ref<ProjectBudget | null>(null);

// 预算表单数据
const budgetFormData = reactive<ProjectBudgetForm>({
  project_id: 0, // 修复：使用默认值 0 而不是直接引用 props
  name: '',
  amount: 0,
  year: new Date().getFullYear(),
  type: '',
  remark: ''
});

// 预算表单规则
const budgetFormRules = {
  name: [
    { required: true, message: '请输入预算名称', trigger: 'blur' }
  ],
  amount: [
    { required: true, message: '请输入金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '金额必须大于等于0', trigger: 'blur' }
  ],
  year: [
    { required: true, message: '请输入预算年度', trigger: 'blur' },
    { type: 'number', message: '请输入有效的年份', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择预算类型', trigger: 'change' }
  ]
};

// 表单标题计算属性
const budgetFormTitle = computed(() => {
  return currentBudget.value ? '编辑预算' : '新增预算';
});

// 修改预算统计数据相关计算属性
const totalBudget = computed(() => {
  return budgets.value.reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

const incomeBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type === 'INCOME')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

const expenseBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type === 'EXPENSE')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

// 统筹预算
const tongchouBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type === 'COORDINATION')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

const otherBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type !== 'INCOME' && budget.type !== 'EXPENSE')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

// 结余经费
const remainingBudget = computed(() => {
  return incomeBudget.value - expenseBudget.value - otherBudget.value - tongchouBudget.value;
});

// 新增格式化的总预算计算属性
const formattedTotalBudget = computed(() => {
  const remaining = incomeBudget.value - expenseBudget.value - otherBudget.value;
  return {
    value: totalBudget.value,
    formatted: `项目预算 ${incomeBudget.value.toFixed(2)}-${expenseBudget.value.toFixed(2)}-${otherBudget.value.toFixed(2)} = ${remaining.toFixed(2)}`
  };
});

// 加载项目详情 - 移到 watch 前面
const loadProjectDetail = async () => {
  projectLoading.value = true;
  try {
    project.value = await projectApi.getProject(props.projectId);
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载项目预算列表 - 移到 watch 前面
const loadProjectBudgets = async () => {
  budgetDataLoading.value = true;
  try {
    const response = await projectBudgetApi.getProjectBudgets({ project_id: props.projectId });
    budgets.value = response.items;
  } catch (error) {
    ElMessage.error('获取预算列表失败');
    console.error('获取预算列表失败:', error);
  } finally {
    budgetDataLoading.value = false;
  }
};

// 监听projectId变化，重新加载数据 - 移到函数定义后面
watch(
  () => props.projectId,
  (newId) => {
    if (newId) {
      budgetFormData.project_id = newId;
      loadProjectDetail();
      loadProjectBudgets();
    }
  },
  { immediate: true }
);

// 加载预算类型选项
const loadBudgetTypeChoices = async () => {
  try {
    budgetTypeChoices.value = await projectBudgetApi.getBudgetTypeChoices();
  } catch (error) {
    ElMessage.error('获取预算类型失败');
    console.error('获取预算类型失败:', error);
  }
};

// 显示预算对话框
const showBudgetDialog = () => {
  currentBudget.value = null;
  // 重置表单数据
  budgetFormData.project_id = props.projectId; // 修复：使用 props.projectId 而不是 projectId
  budgetFormData.name = '';
  budgetFormData.amount = 0;
  budgetFormData.year = new Date().getFullYear();
  budgetFormData.type = '';
  budgetFormData.remark = '';
  budgetDialogVisible.value = true;
};

// 编辑预算
const editBudget = (budget: ProjectBudget) => {
  currentBudget.value = budget;
  // 填充表单数据
  budgetFormData.project_id = budget.project_id;
  budgetFormData.name = budget.name;
  budgetFormData.amount = budget.amount || 0;
  budgetFormData.year = budget.year || new Date().getFullYear();
  budgetFormData.type = budget.type;
  budgetFormData.remark = budget.remark || '';
  budgetDialogVisible.value = true;
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
    loadProjectBudgets();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除预算失败:', error);
    }
  }
};

// 提交预算表单
const submitBudgetForm = async () => {
  if (!budgetFormRef.value) return;
  
  try {
    await budgetFormRef.value.validate();
    
    if (currentBudget.value) {
      // 编辑模式
      await projectBudgetApi.updateProjectBudget(currentBudget.value.id, budgetFormData);
      ElMessage.success('更新成功');
    } else {
      // 新增模式
      await projectBudgetApi.createProjectBudget(budgetFormData);
      ElMessage.success('创建成功');
    }
    
    budgetDialogVisible.value = false;
    loadProjectBudgets();
  } catch (error) {
    ElMessage.error(currentBudget.value ? '更新失败' : '创建失败');
    console.error('提交表单失败:', error);
  }
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

// 格式化日期
const formatDate = (dateStr?: string): string => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString();
};

// 格式化日期时间
const formatDateTime = (dateStr?: string): string => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

// 编辑项目
const handleEdit = () => {
  router.push(`/project/edit/${projectId}`);
};

// 返回上一页（在对话框中改为关闭）
const handleBack = () => {
  emit('close');
};

// 初始化数据 - 现在通过watch监听props变化来加载数据，这里可以移除
// onMounted(() => {
//   loadProjectDetail();
//   loadProjectBudgets();
//   loadBudgetTypeChoices();
// });

// 确保加载预算类型选项
onMounted(() => {
  loadBudgetTypeChoices();
});
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card,
.budget-card {
  background-color: #fff;
}

.budget-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.budget-summary {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
}

.stat-item {
  text-align: center;
  padding: 10px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-value.income {
  color: #67c23a;
}

.stat-value.expense {
  color: #f56c6c;
}

.stat-value.other {
  color: #e6a23c;
}
</style>