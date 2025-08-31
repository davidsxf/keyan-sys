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
        <el-form-item label="项目状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
            <el-option
              v-for="item in statusChoices"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadProjects">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>


      <!-- 项目表格 -->
      <el-table :data="projects" v-loading="loading">
        <el-table-column prop="number" label="项目编号" width="120" />
        <el-table-column prop="title" label="项目名称" min-width="200" />
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


      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadProjects"
          @current-change="loadProjects"
        />
      </div>
    </el-card>


    <!-- 项目表单对话框 -->
    <project-form-dialog
      v-model="dialogVisible"
      :project="currentProject"
      :status-choices="statusChoices"
      :undertake-choices="undertakeChoices"
      @success="handleFormSuccess"
    />
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Project, ProjectFilter } from '@/api/project';
import { projectApi } from '@/api/project';
import ProjectFormDialog from './ProjectFormDialog.vue';


const projects = ref<Project[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentProject = ref<Project | null>(null);
const statusChoices = ref<any[]>([]);
const undertakeChoices = ref<any[]>([]);


const filterForm = ref<ProjectFilter>({
  title: '',
  number: '',
  status: '',
});


const pagination = ref({
  current: 1,
  size: 10,
  total: 0,
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
    
    // 添加分页参数
    params.page = pagination.value.current;
    params.size = pagination.value.size;
    
    const response = await projectApi.getProjects(params);
    console.log('response', response);
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
    const [statusRes, undertakeRes] = await Promise.all([
      projectApi.getStatusChoices(),
      projectApi.getUndertakeChoices(),
    ]);
    statusChoices.value = statusRes;
    undertakeChoices.value = undertakeRes;
  } catch (error) {
    ElMessage.error('获取选项数据失败');
  }
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


// 表单提交成功处理
const handleFormSuccess = () => {
  dialogVisible.value = false;
  loadProjects();
};


// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    title: '',
    number: '',
    status: '',
  };
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


.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
