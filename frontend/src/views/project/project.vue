<!-- components/ProjectList.vue -->
<template>
  <div class="project-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目管理</span>
          <el-button type="primary" @click="showDialog">新增项目</el-button>
        </div>
      </template>


      <!-- 搜索表单 -->
      <el-form :model="filterForm" inline>
        <el-form-item label="项目名称">
          <el-input v-model="filterForm.title" placeholder="请输入项目名称" clearable />
        </el-form-item>
        <el-form-item label="项目编号">
          <el-input v-model="filterForm.number" placeholder="请输入项目编号" clearable />
        </el-form-item>
        <!-- 项目负责人 -->
        <el-form-item label="项目负责人">
          <el-select v-model="filterForm.leader_id" placeholder="请选择项目负责人" clearable>
            <el-option
              v-for="item in leaderChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目级别 -->
        <el-form-item label="项目级别">
          <el-select v-model="filterForm.level" placeholder="请选择项目级别" clearable style="width: 120px">
            <el-option
              v-for="item in levelChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目类别 -->
        <el-form-item label="项目类别">
          <el-select v-model="filterForm.type" placeholder="请选择项目类别" clearable style="width: 120px">
            <el-option
              v-for="item in typeChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目类型 -->
        <el-form-item label="项目类型">
          <el-select v-model="filterForm.category_id" placeholder="请选择项目类型" clearable filterable style="width: 120px">
            <el-option
              v-for="item in categoryChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目来源 -->
        <el-form-item label="项目来源">
          <el-select v-model="filterForm.source" placeholder="请选择项目来源" clearable filterable style="width: 120px">
            <el-option
              v-for="item in sourceChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目承担方式 -->
        <el-form-item label="项目承担方式">
          <el-select v-model="filterForm.undertake" placeholder="请选择承担方式" clearable style="width: 100px">
            <el-option
              v-for="item in undertakeChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!-- 项目状态 -->
        <el-form-item label="项目状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable style="width: 100px">
            <el-option
              v-for="item in statusChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
<!-- 开始日期 -->
<el-form-item label="开始日期">
  <el-date-picker
    v-model="filterForm.start_date"
    type="date"
    placeholder="请选择开始日期"
    clearable
  />
</el-form-item>
<!-- 结束日期 -->
<el-form-item label="结束日期">
  <el-date-picker
    v-model="filterForm.end_date"
    type="date"
    placeholder="请选择结束日期"
    clearable
  />
</el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadProjects">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>


      <!-- 项目表格 -->
      <el-table :data="projects" v-loading="loading">
        <el-table-column prop="number" label="项目编号" width="120" />
        <el-table-column prop="title" label="项目名称" min-width="200">
          <template #default="{ row }">
            <a href="javascript:void(0)" class="project-title-link" @click="showProjectDetail(row)">
              {{ row.title }}
            </a>
          </template>
        </el-table-column>
        <el-table-column prop="leader_name" label="负责人" width="100" />
        <el-table-column prop="status_display" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">{{ row.status_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="budget" label="预算(万元)" width="120" align="right">
          <template #default="{ row }">
            {{ row.budget ? formatCurrency(row.budget) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="undertake_display" label="承担方式" width="100" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editProject(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteProject(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 添加预算统计信息 -->
      <div class="budget-summary">
        <div class="summary-item">
          <span class="summary-label">统计预算(万元) 总数：</span>
          <span class="summary-value">{{ formatCurrency(totalBudget) }}</span>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total || 0" 
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadProjects"
          @current-change="loadProjects"
        />
      </div>
    </el-card>


    <!-- 项目表单对话框 -->
    <!-- 在项目表单对话框后添加详情对话框 -->
    <project-form-dialog
      v-model="dialogVisible"
      :project="currentProject"
      :status-choices="statusChoices"
      :undertake-choices="undertakeChoices"
      @success="handleFormSuccess"
    />
    
    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="项目详情"
      width="70%"
      @close="resetDetailDialog"
    >
      <div v-if="selectedProject" class="project-detail">
    
        <el-descriptions title="基本信息" :column="2"> <!-- 使用v-bind或简写:column="2"确保传递数字类型 -->
          <el-descriptions-item label="项目编号">{{ selectedProject.number }}</el-descriptions-item>
          <el-descriptions-item label="项目名称">{{ selectedProject.title }}</el-descriptions-item>
          <el-descriptions-item label="项目负责人">{{ selectedProject.leader_name }}</el-descriptions-item>
          <el-descriptions-item label="项目状态"><el-tag :type="getStatusTagType(selectedProject.status)">{{ selectedProject.status_display }}</el-tag></el-descriptions-item>
<el-descriptions-item label="项目级别">{{ selectedProject.level_name || '-' }}</el-descriptions-item> <!-- 添加项目级别显示，设置默认值 -->

          <el-descriptions-item label="项目类别">{{ selectedProject.type_name || '-' }}</el-descriptions-item> <!-- 添加默认显示值 -->
                    <el-descriptions-item label="项目类型">{{ selectedProject.category_name || '-' }}</el-descriptions-item> <!-- 添加默认显示值 -->
          <el-descriptions-item label="项目来源">{{ selectedProject.source_name || '-' }}</el-descriptions-item> <!-- 添加默认显示值 -->
          <el-descriptions-item label="承担方式">{{ selectedProject.undertake_display }}</el-descriptions-item>
          <el-descriptions-item label="预算(万元)">{{ selectedProject.budget ? formatCurrency(selectedProject.budget) : '-' }}</el-descriptions-item>
          <el-descriptions-item label="研究领域">{{ selectedProject.research_area || '-' }}</el-descriptions-item>
          <el-descriptions-item label="开始日期">{{ selectedProject.start_date }}</el-descriptions-item>
          <el-descriptions-item label="结束日期">{{ selectedProject.end_date }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedProject.remark || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox, ElDialog, ElDescriptions, ElDescriptionsItem, ElTag } from 'element-plus';
import { Project, ProjectFilter } from '@/api/project';
import { projectApi } from '@/api/project';
import ProjectFormDialog from './ProjectFormDialog.vue';


const projects = ref<Project[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentProject = ref<Project | null>(null);
const statusChoices = ref<any[]>([]);
const undertakeChoices = ref<any[]>([]);
const levelChoices = ref<any[]>([]); // 项目级别选择
const typeChoices = ref<any[]>([]); // 项目类别选择
// 项目详情对话框相关变量
const detailDialogVisible = ref(false);
const selectedProject = ref<Project | null>(null);

const sourceChoices = ref<any[]>([]); // 项目来源选择

const filterForm = ref<ProjectFilter>({
  title: '',
  number: '',
  level: '', // 项目级别
  type: '', // 项目类别
  category_id: null,
  source: null,
  undertake: '',
  status: '',
  leader_id: null,
  start_date: null,
  end_date: null,
});
const categoryChoices = ref<any[]>([]);
const leaderChoices = ref<any[]>([]);


const pagination = ref({
  current: 1,
  size: 10,
  total: 0,
});

// 计算预算总数
const totalBudget = computed(() => {
  return projects.value.reduce((sum, project) => {
    return sum + (project.budget || 0);
  }, 0);
});


// 加载项目列表
const loadProjects = async () => {
  try {
    loading.value = true;
    // 创建只包含非空属性的参数对象
    const params: any = {};
    
    // 只添加非空的filterForm属性
    if (filterForm.value.title) {
      params.title = filterForm.value.title;
    }
    if (filterForm.value.number) {
      params.number = filterForm.value.number;
    }
    if (filterForm.value.status) {
      params.status = filterForm.value.status;
    }
    if (filterForm.value.category_id) {
      params.category_id = filterForm.value.category_id;
    }
    if (filterForm.value.source) {
      params.source = filterForm.value.source;
    }
    if (filterForm.value.undertake) {
      params.undertake = filterForm.value.undertake;
    }
    // 添加缺失的字段处理
    if (filterForm.value.leader_id) {
      params.leader_id = filterForm.value.leader_id;
    }
    // 添加项目级别和类别的筛选
    if (filterForm.value.level) {
      params.level = filterForm.value.level;
    }
    if (filterForm.value.type) {
      params.type = filterForm.value.type;
    }
    // 修复日期格式问题，确保日期转换为字符串
    if (filterForm.value.start_date) {
      const date = new Date(filterForm.value.start_date);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      params.start_date = `${year}-${month}-${day}`;
    }
    if (filterForm.value.end_date) {
      const date = new Date(filterForm.value.end_date);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      params.end_date = `${year}-${month}-${day}`;
    }
    
    // 添加分页参数
    params.page = pagination.value.current;
    params.size = pagination.value.size;

    const response = await projectApi.getProjects(params);
    projects.value = response.items;
    pagination.value.total = response.total;
  } catch (error) {
    ElMessage.error('获取项目列表失败');
  } finally {
    loading.value = false;
  }
};


// 加载选项数据
const loadChoices = async () => {
  try {
    const [statusRes, undertakeRes, categoryRes, typeRes, leaderRes, levelRes, sourceRes] = await Promise.all([
      projectApi.getStatusChoices(),
      projectApi.getUndertakeChoices(),
      projectApi.getCategoryChoices(),
      projectApi.getTypeChoices(),
      projectApi.getLeaderChoices(),
      projectApi.getLevelChoices(), // 加载项目级别选项
      projectApi.getSourceChoices() // 加载项目来源选项
    ]);
    statusChoices.value = statusRes;
    undertakeChoices.value = undertakeRes;
    categoryChoices.value = categoryRes;
    typeChoices.value = typeRes; // 项目类别选项
    leaderChoices.value = leaderRes;
    levelChoices.value = levelRes; // 项目级别选项
    sourceChoices.value = sourceRes; // 项目来源选项
  } catch (error) {
    ElMessage.error('获取选项数据失败');
  }
};

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    title: '',
    number: '',
    status: '',
    category_id: null,
    source: null,
    undertake: '',
    leader_id: null,
    start_date: null,
    end_date: null,
    level: '', // 重置项目级别
    type: '' // 重置项目类别
  };
  loadProjects();
};


// 显示新增对话框
const showDialog = () => {
  currentProject.value = null;
  dialogVisible.value = true;
};


// 编辑项目
const editProject = (project: Project) => {
  currentProject.value = project;
  dialogVisible.value = true;
};


// 删除项目
const deleteProject = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${project.title}" 吗？`,
      '删除确认',
      { type: 'warning' }
    );
    
    await projectApi.deleteProject(project.id);
    ElMessage.success('删除成功');
    loadProjects();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

// 显示项目详情
const showProjectDetail = (project: Project) => {
  
  selectedProject.value = project;
  console.log('selectedProject.value', selectedProject.value);
  detailDialogVisible.value = true;
};

// 重置详情对话框
const resetDetailDialog = () => {
  selectedProject.value = null;
};

// 表单提交成功处理
const handleFormSuccess = () => {
  dialogVisible.value = false;
  loadProjects();
};


// 状态标签类型
const getStatusTagType = (status: string) => {
  const map: { [key: string]: string } = {
    APPROVED: 'warning',
    IN_PROGRESS: 'primary',
    COMPLETED: 'success',
    TERMINATED: 'danger',
  };
  return map[status] || 'info';
};


// 格式化金额
const formatCurrency = (value: number) => {
  return value.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};


onMounted(() => {
  loadProjects();
  loadChoices();
});
</script>


<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 预算统计样式 */
.budget-summary {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  display: flex;
  justify-content: flex-end;
}

.summary-item {
  display: flex;
  align-items: center;
}

.summary-label {
  margin-right: 5px;
  font-weight: 500;
}

.summary-value {
  font-weight: bold;
  color: #409eff;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
    /* 确保分页容器可见 */
  height: 40px;
  width: 100%;
  overflow: visible;
}

/* 项目链接样式 */
.project-title-link {
  color: #409eff;
  text-decoration: none;
}

.project-title-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

/* 项目详情样式 */
.project-detail {
  padding: 10px 0;
}
</style>
