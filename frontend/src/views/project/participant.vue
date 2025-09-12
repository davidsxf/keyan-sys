<template>
  <div class="participant-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目参与人员管理</span>
          <el-button type="primary" @click="showDialog">新增参与人员</el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :model="filterForm" inline>
        <el-form-item label="项目ID">
          <el-input v-model.number="filterForm.project_id" placeholder="请输入项目ID" clearable />
        </el-form-item>
        <el-form-item label="员工ID">
          <el-input v-model.number="filterForm.staff_id" placeholder="请输入员工ID" clearable />
        </el-form-item>
        <el-form-item label="员工姓名">
          <el-input v-model="filterForm.staff_name" placeholder="请输入员工姓名" clearable />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="filterForm.role" placeholder="请选择角色" clearable>
            <el-option
              v-for="role in roleChoices"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadParticipants">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 参与人员表格 -->
      <el-table :data="participants" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="project_id" label="项目ID" width="100" />
        <el-table-column prop="project_title" label="项目名称" min-width="200">
          <template #default="{ row }">
            <a href="javascript:void(0)" class="project-title-link" @click="showProjectDetail(row.project_id)">
              {{ row.project_title || '-' }}
            </a>
          </template>
        </el-table-column>
        <el-table-column prop="staff_id" label="员工ID" width="100" />
        <el-table-column prop="staff_name" label="员工姓名" width="120" />
        <el-table-column prop="staff_department" label="所属部门" width="150" />
        <el-table-column prop="role_display" label="角色" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.role_display || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order" label="排序" width="80" />
        <el-table-column prop="join_date" label="加入日期" width="120" />
        <el-table-column prop="leave_date" label="离开日期" width="120" />
        <el-table-column prop="remark" label="备注" min-width="150" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editParticipant(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteParticipant(row)">删除</el-button>
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
          @size-change="loadParticipants"
          @current-change="loadParticipants"
        />
      </div>
    </el-card>

    <!-- 参与人员表单对话框 -->
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
        <el-form-item label="项目" prop="project_id">
          <el-select 
            v-model="formData.project_id" 
            placeholder="请选择项目"
            filterable
            remote
            :remote-method="remoteSearchProjects"
            :loading="projectLoading"
            value-key="id"
            clearable
            @visible-change="handleProjectSelectVisibleChange"
          >
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.title"
              :value="project.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="员工" prop="staff_id">
          <el-select 
            v-model="formData.staff_id" 
            placeholder="请选择员工"
            filterable
            remote
            :remote-method="remoteSearchStaff"
            :loading="staffLoading"
            value-key="id"
            clearable
            @visible-change="handleStaffSelectVisibleChange"
          >
            <el-option
              v-for="staff in staffs"
              :key="staff.id"
              :label="staff.name"
              :value="staff.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色">
            <el-option
              v-for="role in roleChoices"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="排序">
          <el-input-number
            v-model.number="formData.order"
            :min="0"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="加入日期">
          <el-date-picker
            v-model="formData.join_date"
            type="date"
            placeholder="请选择加入日期"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="离开日期">
          <el-date-picker
            v-model="formData.leave_date"
            type="date"
            placeholder="请选择离开日期"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="formData.remark"
            type="textarea"
            placeholder="请输入备注信息"
            :rows="3"
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
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';
import type { FormInstance } from 'element-plus';
import { participantApi } from '@/api/participant';
import { projectApi } from '@/api/project';
import { staffApi } from '@/api/staff';
import type { ProjectStaff, ProjectStaffForm, ProjectStaffFilter, Choice } from '@/api/participant';
import type { Project } from '@/api/project';
import type { Staff } from '@/api/staff';

const router = useRouter();

// 数据加载状态
const loading = ref(false);

// 参与人员列表
const participants = ref<ProjectStaff[]>([]);

// 分页信息
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 筛选表单
const filterForm = reactive<ProjectStaffFilter>({});

// 角色选项
const roleChoices = ref<Choice[]>([]);

// 对话框状态
const dialogVisible = ref(false);
const formRef = ref<FormInstance>();
const currentParticipant = ref<ProjectStaff | null>(null);

// 表单数据
const formData = reactive<ProjectStaffForm>({
  project_id: 0,
  staff_id: 0,
  role: '',
  order: undefined,
  join_date: undefined,
  leave_date: undefined,
  remark: undefined
});

// 表单规则
const formRules = reactive({
  project_id: [
    { required: true, message: '请选择项目', trigger: 'change' },
    { type: 'number', message: '项目ID必须为数字', trigger: 'change' }
  ],
  staff_id: [
    { required: true, message: '请选择员工', trigger: 'change' },
    { type: 'number', message: '员工ID必须为数字', trigger: 'change' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
});

// 表单标题
const formTitle = computed(() => {
  return currentParticipant.value ? '编辑参与人员' : '新增参与人员';
});

// 项目列表和加载状态
const projects = ref<Project[]>([]);
const projectLoading = ref(false);

// 员工列表和加载状态
const staffs = ref<Staff[]>([]);
const staffLoading = ref(false);

// 加载参与人员列表
const loadParticipants = async () => {
  loading.value = true;
  try {
    const params = {
      ...filterForm,
      page: pagination.current,
      size: pagination.size
    };
    const response = await participantApi.getParticipants(params);
    participants.value = response.items || [];
    pagination.total = response.total || 0;
  } catch (error) {
    ElMessage.error('获取参与人员列表失败');
    console.error('获取参与人员列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 加载角色选项
const loadRoleChoices = async () => {
  try {
    roleChoices.value = await participantApi.getParticipantRoles();
  } catch (error) {
    ElMessage.error('获取角色选项失败');
    console.error('获取角色选项失败:', error);
  }
};

// 加载所有项目
const loadAllProjects = async () => {
  projectLoading.value = true;
  try {
    // 获取所有项目，不使用搜索条件
    const response = await projectApi.getProjects({});
    projects.value = response.items || [];
  } catch (error) {
    ElMessage.error('加载项目列表失败');
    console.error('加载项目列表失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 远程搜索项目
const remoteSearchProjects = async (query: string) => {
  if (!query) {
    // 如果查询为空，加载所有项目
    await loadAllProjects();
    return;
  }
  
  projectLoading.value = true;
  try {
    const response = await projectApi.getProjects({ title: query });
    projects.value = response.items || [];
  } catch (error) {
    ElMessage.error('搜索项目失败');
    console.error('搜索项目失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载所有员工
const loadAllStaffs = async () => {
  staffLoading.value = true;
  try {
    // 获取所有员工，不使用搜索条件
    const response = await staffApi.getStaffs('', undefined, undefined, undefined, 1, 100);
    staffs.value = response || [];
  } catch (error) {
    ElMessage.error('加载员工列表失败');
    console.error('加载员工列表失败:', error);
  } finally {
    staffLoading.value = false;
  }
};

// 远程搜索员工
const remoteSearchStaff = async (query: string) => {
  if (!query) {
    // 如果查询为空，加载所有员工
    await loadAllStaffs();
    return;
  }
  
  staffLoading.value = true;
  try {
    const response = await staffApi.getStaffs(query, undefined, undefined, undefined, 1, 50);
    staffs.value = response || [];
  } catch (error) {
    ElMessage.error('搜索员工失败');
    console.error('搜索员工失败:', error);
  } finally {
    staffLoading.value = false;
  }
};

// 处理员工选择框显示/隐藏事件
const handleStaffSelectVisibleChange = async (visible: boolean) => {
  if (visible) {
    // 当下拉框显示时，加载所有员工
    await loadAllStaffs();
  }
};

// 处理项目选择框显示/隐藏事件
const handleProjectSelectVisibleChange = async (visible: boolean) => {
  if (visible) {
    // 当下拉框显示时，加载所有项目
    await loadAllProjects();
  }
};

// 重置筛选条件
const resetFilter = () => {
  Object.keys(filterForm).forEach(key => {
    (filterForm as any)[key] = undefined;
  });
  loadParticipants();
};

// 显示对话框
const showDialog = () => {
  currentParticipant.value = null;
  // 重置表单数据
  Object.keys(formData).forEach(key => {
    (formData as any)[key] = key === 'project_id' || key === 'staff_id' ? 0 : undefined;
  });
  dialogVisible.value = true;
};

// 编辑参与人员
const editParticipant = async (participant: ProjectStaff) => {
  currentParticipant.value = participant;
  // 填充表单数据
  formData.project_id = participant.project_id;
  formData.staff_id = participant.staff_id;
  formData.role = participant.role;
  formData.order = participant.order;
  formData.join_date = participant.join_date;
  formData.leave_date = participant.leave_date;
  formData.remark = participant.remark;
  dialogVisible.value = true;
};

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    console.log('formData:', formData);
    if (currentParticipant.value) {
      // 更新参与人员
      await participantApi.updateParticipant(currentParticipant.value.id, formData);
      ElMessage.success('参与人员更新成功');
    } else {
      // 创建参与人员
      await participantApi.createParticipant(formData);
      ElMessage.success('参与人员创建成功');
    }
    
    dialogVisible.value = false;
    loadParticipants();
  } catch (error) {
    const axiosError = error as any;
    const errorMessage = axiosError.response?.data?.detail || axiosError.message || '操作失败';
    
    // 只记录错误但不显示给用户
    console.error('提交表单失败:', errorMessage);
  }
};

// 删除参与人员
const deleteParticipant = async (participant: ProjectStaff) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除参与人员(ID: ${participant.id})吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );
    
    await participantApi.deleteParticipant(participant.id);
    ElMessage.success('参与人员删除成功');
    loadParticipants();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除参与人员失败:', error);
    }
  }
};

// 查看项目详情
const showProjectDetail = (projectId: number) => {
  router.push(`/project/detail/${projectId}`);
};

// 初始加载
onMounted(() => {
  loadParticipants();
  loadRoleChoices();
});
</script>

<style scoped>
.participant-list {
  padding: 20px;
}

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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.project-title-link {
  color: #409eff;
  text-decoration: none;
}

.project-title-link:hover {
  text-decoration: underline;
}
</style>