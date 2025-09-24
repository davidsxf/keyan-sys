<template>
  <div class="project-detail-page">
    <!-- 项目详细信息部分 -->
    <el-card class="project-info-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 20px;">
            <span>项目详细信息</span>
            <el-select
              v-model="selectedProjectId"
              placeholder="请选择项目"
              style="width: 300px;"
              :loading="projectsLoading"
              @change="handleProjectChange"
              filterable
              clearable
            >
              <el-option
                v-for="item in projects"
                :key="item.id"
                :label="`${item.number} - ${item.title}`"
                :value="item.id"
              />
            </el-select>
          </div>
          <div class="header-actions">
            <!-- <el-button @click="handleBack">返回列表</el-button> -->
            <el-button type="primary" @click="handleEdit">编辑项目</el-button>
            
        </div>
        </div>
      </template>
      
      <div v-if="project" class="project-info-content">
        <el-descriptions title="基本信息" :column="3" border>
          <el-descriptions-item label="项目编号" :span="1">{{ project.number }}</el-descriptions-item>
          <el-descriptions-item label="项目名称" :span="2">{{ project.title }}</el-descriptions-item>
          <el-descriptions-item label="项目负责人" :span="1">{{ project.leader_name }}</el-descriptions-item>
          <el-descriptions-item label="项目状态" :span="1">
            <el-tag :type="getStatusTagType(project.status)">{{ project.status_display }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="项目类别" :span="1">{{ project.category_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="项目类型" :span="1">{{ project.type_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="项目来源" :span="1">{{ project.source_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="承担方式" :span="1">{{ project.undertake_display }}</el-descriptions-item>
          <el-descriptions-item label="预算(万元)" :span="1">{{ project.budget ? formatCurrency(project.budget) : '-' }}</el-descriptions-item>
          <el-descriptions-item label="经费编号" :span="1">{{ project.funding_number || '-' }}</el-descriptions-item>
          <el-descriptions-item label="开始日期" :span="1">{{ project.start_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="结束日期" :span="1">{{ project.end_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="研究领域" :span="3">{{ project.research_area || '-' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="3">{{ project.remark || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <div v-else class="no-data">
        <el-empty description="暂无项目数据" />
      </div>
    </el-card>
    
    <!-- Tab分页部分 -->
    <el-card class="project-tabs-card" style="margin-top: 20px;">
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="项目经费" name="budget">
          <div class="tab-content">
            <div class="tab-header">
              <span>经费列表</span>
              <el-button type="primary" @click="showBudgetDialog">新增经费</el-button>
            </div>
            
            <!-- 预算搜索表单 -->
            <el-form :model="budgetFilter" inline style="margin-bottom: 15px;">
              
              <el-form-item label="年度" style="width: 200px;">
                <el-select v-model="budgetFilter.year" placeholder="请选择年度" clearable @change="loadProjectBudgets">
                  <el-option
                    v-for="item in yearOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item>
       
                <el-button @click="resetBudgetFilter">重置</el-button>
              </el-form-item>
            </el-form>
            
            <!-- 预算统计 -->
            <div class="budget-stats" style="margin-bottom: 15px;">
              <el-row :gutter="20">
                  <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">合同经费</span>
                    <span class="stat-value income">{{ formatCurrency(project?.budget || 0) }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">到账经费</span>
                    <span class="stat-value income">{{ formatCurrency(incomeBudget) }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">外拨经费</span>
                    <span class="stat-value expense">{{ formatCurrency(expenseBudget) }}</span>
                  </div>
                </el-col>
 
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">留所经费</span>
                    <span class="stat-value net">{{ formatCurrency(netBudget) }}</span>
                  </div>
                </el-col>
              </el-row>
            </div>
            
            <!-- 预算表格 -->
            <el-table :data="budgets" v-loading="budgetsLoading">
              <el-table-column prop="name" label="经费名称" width="180" />
              <el-table-column prop="amount" label="金额(万元)" width="120" align="right">
                <template #default="{ row }">
                  {{ formatCurrency(row.amount || 0) }}
                </template>
              </el-table-column>
              <el-table-column prop="year" label="年度" width="100" />
              <el-table-column prop="type" label="类型" width="120">
                <template #default="{ row }">
                  {{ getBudgetTypeDisplay(row.type) }}
                </template>
              </el-table-column>
              <el-table-column prop="remark" label="备注" min-width="200" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="editBudget(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteBudget(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 预算分页 -->
            <div class="pagination" style="margin-top: 15px;">
              <el-pagination
                v-model:current-page="budgetPagination.current"
                v-model:page-size="budgetPagination.size"
                :total="budgetPagination.total || 0"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadProjectBudgets"
                @current-change="loadProjectBudgets"
              />
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="项目参与人员" name="participant">
          <div class="tab-content">
            <div class="tab-header">
              <span>参与人员列表</span>
              <el-button type="primary" @click="showParticipantDialog">新增人员</el-button>
            </div>
            
            <!-- 参与人员搜索表单 -->
   
            
            <!-- 参与人员表格 -->
            <el-table :data="participants" v-loading="participantsLoading">
              <el-table-column prop="staff_name" label="员工姓名" width="120" />
              <el-table-column prop="staff_number" label="员工编号" width="120" />
              <el-table-column prop="department_name" label="所属部门" width="150" />
              <el-table-column prop="role_display" label="角色" width="120">
                <template #default="{ row }">
                  <el-tag>{{ row.role_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="join_date" label="加入日期" width="120" />
              <el-table-column prop="remark" label="备注" min-width="200" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="editParticipant(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteParticipant(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 参与人员分页 -->
            <div class="pagination" style="margin-top: 15px;">
              <el-pagination
                v-model:current-page="participantPagination.current"
                v-model:page-size="participantPagination.size"
                :total="participantPagination.total || 0"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadProjectParticipants"
                @current-change="loadProjectParticipants"
              />
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="项目文档" name="document">
          <div class="tab-content">
            <div class="tab-header">
              <span>文档列表</span>
              <el-button type="primary" @click="showDocumentDialog">上传文档</el-button>
            </div>
            
            <!-- 文档搜索表单 -->
            <el-form :model="documentFilter" inline style="margin-bottom: 15px;">
              <el-form-item label="文档名称">
                <el-input v-model="documentFilter.name" placeholder="请输入文档名称" clearable />
              </el-form-item>
              <el-form-item label="上传日期">
                <el-date-picker
                  v-model="documentFilter.upload_date"
                  type="date"
                  placeholder="请选择上传日期"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="loadProjectDocuments">搜索</el-button>
                <el-button @click="resetDocumentFilter">重置</el-button>
              </el-form-item>
            </el-form>
            
            <!-- 文档表格 -->
            <el-table :data="documents" v-loading="documentsLoading">
              <el-table-column prop="name" label="文档名称" min-width="200" />
              <el-table-column prop="file_size" label="文件大小" width="100">
                <template #default="{ row }">
                  {{ formatFileSize(row.file_size) }}
                </template>
              </el-table-column>
              <el-table-column prop="file_type" label="文件类型" width="100" />
              <el-table-column prop="upload_by_name" label="上传人" width="120" />
              <el-table-column prop="upload_date" label="上传日期" width="150" />
              <el-table-column prop="remark" label="备注" min-width="200" />
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="downloadDocument(row.file_path, row.name)">下载</el-button>
                  <el-button size="small" type="danger" @click="deleteDocument(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 文档分页 -->
            <div class="pagination" style="margin-top: 15px;">
              <el-pagination
                v-model:current-page="documentPagination.current"
                v-model:page-size="documentPagination.size"
                :total="documentPagination.total || 0"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadProjectDocuments"
                @current-change="loadProjectDocuments"
              />
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="项目负责人变更" name="leaderChange">
          <div class="tab-content">
            <div class="tab-header">
              <span>负责人变更记录</span>
              <el-button type="primary" @click="showChangeLeaderDialog">变更负责人</el-button>
            </div>
            <!-- 负责人变更记录表格 -->
            <el-table :data="leaderChanges" v-loading="leaderChangesLoading">
              <el-table-column prop="change_date" label="变更日期" width="150" />

              <el-table-column prop="new_leader_name" label="变更后负责人" width="250" />
              <el-table-column prop="remark" label="备注" min-width="300" />
            </el-table>
    
          </div>
        </el-tab-pane>
        
  
      </el-tabs>
    </el-card>
    
    <!-- 预算表单对话框 -->
    <el-dialog
      v-model="budgetDialogVisible"
      :title="budgetDialogTitle"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="budgetFormRef"
        :model="budgetForm"
        :rules="budgetFormRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="预算名称" prop="name">
          <el-input v-model="budgetForm.name" placeholder="请输入预算名称" />
        </el-form-item>
        <el-form-item label="年度" prop="year">
          <el-select v-model="budgetForm.year" placeholder="请选择年度">
            <el-option v-for="year in yearOptions" :key="year.value" :label="year.label" :value="year.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="预算类型" prop="type">
       <el-select v-model="budgetForm.type" placeholder="请选择预算类型">
            <el-option v-for="choice in budgetTypeChoices" :key="choice.value" :label="choice.label" :value="choice.value" />
          </el-select>
        </el-form-item>

        
        <el-form-item label="预算金额" prop="amount">
          <el-input-number
            v-model.number="budgetForm.amount"
            :min="0"
            :precision="2"
            :step="0.1"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="budgetForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="budgetDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBudgetForm">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 参与人员表单对话框 -->
    <el-dialog
      v-model="participantDialogVisible"
      :title="participantDialogTitle"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="participantFormRef"
        :model="participantForm"
        :rules="participantFormRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="员工" prop="staff_id">
          <el-select
            v-model="participantForm.staff_id"
            placeholder="请选择员工"
            filterable
            remote
            :remote-method="remoteSearchStaff"
            :loading="staffLoading"
            @visible-change="handleStaffSelectVisibleChange"
          >
            <el-option
              v-for="staff in staffOptions"
              :key="staff.id"
              :label="staff.name"
              :value="staff.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="participantForm.role" placeholder="请选择角色">
            <el-option
              v-for="role in roleChoices"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="加入日期" prop="join_date">
          <el-date-picker
            v-model="participantForm.join_date"
            type="date"
            placeholder="选择加入日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="participantForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="participantDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitParticipantForm">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 文档表单对话框 -->
    <el-dialog
      v-model="documentDialogVisible"
      :title="documentDialogTitle"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="documentFormRef"
        :model="documentForm"
        :rules="documentFormRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="文档名称" prop="name">
          <el-input v-model="documentForm.name" placeholder="请输入文档名称" />
        </el-form-item>
        <el-form-item label="上传文件" prop="file">
          <el-upload
            ref="upload"
            :auto-upload="false"
            :file-list="fileList"
            :before-upload="handleFileBeforeUpload"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :limit="1"
            class="upload-demo"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能上传单个文件，支持常见文档格式
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="documentForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeDocumentDialog">取消</el-button>
        <el-button type="primary" @click="submitDocumentForm">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 变更负责人对话框 -->
    <el-dialog
        v-model="changeLeaderDialogVisible"
        title="变更项目负责人"
        width="500px"
        :before-close="handleCloseChangeLeaderDialog"
    >
        <el-form
            ref="changeLeaderFormRef"
            :model="{ newLeaderId, changeRemark }"
            label-width="100px"
            style="padding-top: 20px;"
        >
            <el-form-item
                label="当前负责人"
                disabled
            >
                <span>{{ project?.leader_name || '-' }}</span>
            </el-form-item>
            <el-form-item
                label="新负责人"
                prop="newLeaderId"
                :rules="[{ required: true, message: '请选择新负责人', trigger: 'change' }]"
            >
                <el-select
                    v-model="newLeaderId"
                    placeholder="请选择新负责人"
                    style="width: 100%;"
                    filterable
                    loading="loadingLeaders"
                >
                    <el-option
                        v-for="item in leaderOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item
                label="变更时间"
                prop="changeDate"
            >
                <el-date-picker
                    v-model="changeDate"
                    type="date"
                    placeholder="选择变更时间"
                    value-format="YYYY-MM-DD"
                    style="width: 100%;"
                />
            </el-form-item>
            <el-form-item
                label="变更备注"
                prop="changeRemark"
            >
                <el-input
                    v-model="changeRemark"
                    type="textarea"
                    placeholder="请输入变更原因（选填）"
                    :rows="3"
                />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="changeLeaderDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmChangeLeader">确定</el-button>
            </span>
        </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox, FormInstance, FormRules, UploadFile, UploadRawFile } from 'element-plus';
import { Project } from '@/api/project';
import { projectApi } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';
import { participantApi } from '@/api/participant';
import * as documentApi from '@/api/document';
import { staffApi } from '@/api/staff';
import { downloadFile } from '@/utils/http';
// import Project from './project.vue';

// 路由和参数
const route = useRoute();
const router = useRouter();
const selectedProjectId = ref(Number(route.query.id || 0));

// 添加项目列表相关变量
const projects = ref<any[]>([]);
const projectsLoading = ref(false);

// 项目数据
const project = ref<Project | null>(null);
const projectLoading = ref(false);

// 活动标签页
const activeTab = ref('budget');

// 变更负责人相关状态
const changeLeaderDialogVisible = ref(false);
const newLeaderId = ref<number | null>(null);
const changeRemark = ref('');
const leaderOptions = ref<any[]>([]);
const loadingLeaders = ref(false);

// 预算相关
const budgets = ref<any[]>([]);
const budgetsLoading = ref(false);
const budgetPagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const budgetFilter = reactive({
  year: ''
});
const budgetDialogVisible = ref(false);
const currentBudget = ref<any | null>(null);
const budgetFormRef = ref<FormInstance>();
const budgetForm = reactive({
  project_id: selectedProjectId.value || undefined,
  name: '',
  year: new Date().getFullYear(), // 默认当前年份
  type: '',
  amount: 0,
  remark: ''
});

// 添加年度选项数据
const yearOptions = ref<any[]>([]);
// 生成最近10年到未来5年的选项
const currentYear = new Date().getFullYear();
for (let i = currentYear - 10; i <= currentYear + 5; i++) {
  yearOptions.value.push({
    label: i + '年',
    value: i
  });
}

// 添加预算类型选项数据
const budgetTypeChoices = ref<any[]>([
  { label: '到账经费', value: 'income' },
  { label: '外拨经费', value: 'expense' }
]);

// 参与人员相关
const participants = ref<any[]>([]);
const participantsLoading = ref(false);
const participantPagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
// const participantFilter = reactive({
//   staff_name: '',
//   role: ''
// });
const participantDialogVisible = ref(false);
const currentParticipant = ref<any | null>(null);
const participantFormRef = ref<FormInstance>();
const participantForm = reactive({
  project_id: selectedProjectId.value || undefined,
  staff_id: undefined,
  role: '',
  join_date: '',
  remark: ''
});
const staffOptions = ref<any[]>([]);
const staffLoading = ref(false);
const roleChoices = ref<any[]>([]);

// 文档相关
const documents = ref<any[]>([]);
const documentsLoading = ref(false);
const documentPagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const documentFilter = reactive({
  name: '',
  upload_date: ''
});
const documentDialogVisible = ref(false);
const currentDocument = ref<any | null>(null);
const documentFormRef = ref<FormInstance>();
const documentForm = reactive({
  name: '',
  file: null as File | null,
  remark: ''
});
const fileList = ref<UploadFile[]>([]);

// 负责人变更相关
const leaderChanges = ref<any[]>([]);
const leaderChangesLoading = ref(false);
const leaderChangePagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const leaderChangeFilter = reactive({
  change_date: ''
});

// 计算属性
const budgetDialogTitle = computed(() => currentBudget.value ? '编辑预算' : '新增预算');
const participantDialogTitle = computed(() => currentParticipant.value ? '编辑参与人员' : '新增参与人员');
const documentDialogTitle = computed(() => currentDocument.value ? '编辑文档' : '上传文档');

// 预算统计计算属性
const incomeBudget = computed(() => {
  return (budgets.value || [])
    .filter(item => item.type === 'income')
    .reduce((sum, item) => sum + (item.amount || 0), 0);
});

const expenseBudget = computed(() => {
  return (budgets.value || [])
    .filter(item => item.type === 'expense')
    .reduce((sum, item) => sum + (item.amount || 0), 0);
});

const netBudget = computed(() => {
  return incomeBudget.value - expenseBudget.value;
});

// 表单验证规则
const budgetFormRules: FormRules = {
  name: [{ required: true, message: '请输入预算名称', trigger: 'blur' }],
  year: [{ required: true, message: '请输入年度', trigger: 'blur' }],
  type: [{ required: true, message: '请选择预算类型', trigger: 'change' }],
  amount: [
    { required: true, message: '请输入金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '金额不能为负数', trigger: 'blur' }
  ]
};

const participantFormRules: FormRules = {
  staff_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  join_date: [{ required: true, message: '请选择加入日期', trigger: 'change' }]
};

const documentFormRules: FormRules = {
  name: [{ required: true, message: '请输入文档名称', trigger: 'blur' }],
  file: [{ required: true, message: '请上传文件', trigger: 'change' }]
};

// 加载项目详情
const loadProjectDetail = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    projectLoading.value = true;
    // 修改这里，将不存在的getProjectDetail改为正确的getProject
    const data = await projectApi.getProject(selectedProjectId.value);
    project.value = data;
  } catch (error) {
    ElMessage.error('加载项目详情失败');
    console.error('加载项目详情失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载项目列表（用于下拉选择）
const loadProjects = async () => {
  try {
    projectsLoading.value = true;
    // 获取所有项目，用于下拉选择
    const { items } = await projectApi.getProjects({
      page: 1,
      page_size: 1000, // 获取足够多的项目
      ordering: '-id'
    });
    projects.value = items;
  } catch (error) {
    ElMessage.error('加载项目列表失败');
    console.error('加载项目列表失败:', error);
  } finally {
    projectsLoading.value = false;
  }
};

// 加载预算数据
const loadProjectBudgets = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    budgetsLoading.value = true;

    const results = await projectBudgetApi.getProjectBudget(selectedProjectId.value) || [];
    
    // 应用年度筛选
    let filteredResults = results;
    if (budgetFilter.year) {
      filteredResults = results.filter(item => item.year === budgetFilter.year);
    }
    
    budgets.value = filteredResults;
    budgetPagination.total = filteredResults.length; // 设置筛选后的总条数
  } catch (error) {
    ElMessage.error('加载预算数据失败');
    console.error('加载预算数据失败:', error);
  } finally {
    budgetsLoading.value = false;
  }
};

// 加载参与人员数据
const loadProjectParticipants = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    participantsLoading.value = true;
    const { results, count } = await participantApi.getProjectParticipants(selectedProjectId.value) || { results: [], count: 0 };
    
    // 确保 results 是一个数组
    participants.value = Array.isArray(results) ? results : [];
    participantPagination.total = count || 0;
    
    // 如果没有数据，可以显示提示信息
    if ((participants.value || []).length === 0) {
      console.log('当前项目没有参与人员数据');
    }
  } catch (error) {
    ElMessage.error('加载参与人员数据失败');
    console.error('加载参与人员数据失败:', error);
    // 出错时确保 participants 是一个空数组
    participants.value = [];
    participantPagination.total = 0;
  } finally {
    participantsLoading.value = false;
  }
};

// 加载文档数据
const loadProjectDocuments = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    documentsLoading.value = true;
    const params = {
      ...documentFilter,
      page: documentPagination.current,
      page_size: documentPagination.size
    };
    const { results, count } = await documentApi.getProjectDocuments(selectedProjectId.value, params);
    documents.value = results;
    documentPagination.total = count;
  } catch (error) {
    ElMessage.error('加载文档数据失败');
    console.error('加载文档数据失败:', error);
  } finally {
    documentsLoading.value = false;
  }
};

// 加载负责人变更记录
const loadProjectLeaderChanges = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    leaderChangesLoading.value = true;
    const params = {
      ...leaderChangeFilter,
      page: leaderChangePagination.current,
      page_size: leaderChangePagination.size
    };
    const { results, count } = await projectApi.getProjectLeaderChanges(selectedProjectId.value, params);
    leaderChanges.value = results;
    leaderChangePagination.total = count;
  } catch (error) {
    ElMessage.error('加载负责人变更记录失败');
    console.error('加载负责人变更记录失败:', error);
  } finally {
    leaderChangesLoading.value = false;
  }
};



// 搜索员工
const remoteSearchStaff = async (query: string) => {
  try {
    staffLoading.value = true;
    const response = await staffApi.getStaffs(query, undefined, undefined, undefined, 1, 100);
    staffOptions.value = response.data.map((staff: any) => ({
      id: staff.id,
      name: staff.name,
      number: staff.number
    }));
  } catch (error) {
    console.error('搜索员工失败:', error);
    ElMessage.error('搜索员工失败，请重试');
  } finally {
    staffLoading.value = false;
  }
};

// 处理员工选择下拉框显示
const handleStaffSelectVisibleChange = (visible: boolean) => {
  if (visible && !staffOptions.value.length) {
    remoteSearchStaff('');
  }
};

// 处理标签页点击
const handleTabClick = (tab: any) => {
  activeTab.value = tab.name;
  
  // 根据选中的标签页加载对应数据
  switch (tab.name) {
    case 'budget':
      loadProjectBudgets();
      break;
    case 'participant':
      loadProjectParticipants();
      break;
    case 'document':
      loadProjectDocuments();
      break;
    case 'leaderChange':
      loadProjectLeaderChanges();
      break;
  }
};

// 预算相关方法
const showBudgetDialog = () => {
  currentBudget.value = null;
  resetBudgetForm();
  budgetDialogVisible.value = true;
};

const editBudget = (row: any) => {
  currentBudget.value = { ...row };
  Object.assign(budgetForm, {
    project_id: selectedProjectId.value || undefined,
    name: row.name || '',
    year: row.year || new Date().getFullYear(), // 编辑时如果没有年份，默认当前年份
    type: row.type || '',
    amount: row.amount || 0,
    remark: row.remark || ''
  });
  budgetDialogVisible.value = true;
};

const deleteBudget = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条预算记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await projectBudgetApi.deleteProjectBudget(row.id);
    ElMessage.success('删除成功');
    loadProjectBudgets();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const submitBudgetForm = async () => {
  if (!budgetFormRef.value) return;
  
  // 先检查项目是否已选择
  if (!budgetForm.project_id) {
    ElMessage.warning('请先选择项目');
    return;
  }
  
  try {
    const valid = await budgetFormRef.value.validate();
    if (!valid) return;
    
    // 验证项目是否存在于项目列表中
    const projectExists = projects.value.some(p => p.id === budgetForm.project_id);
    if (!projectExists) {
      ElMessage.error('选择的项目不存在');
      return;
    }
    
    if (currentBudget.value) {
      // 更新预算
      await projectBudgetApi.updateProjectBudget(currentBudget.value.id, budgetForm);
      ElMessage.success('更新成功');
    } else {
      // 创建预算
      await projectBudgetApi.createProjectBudget(budgetForm);
      ElMessage.success('创建成功');
    }
    
    budgetDialogVisible.value = false;
    loadProjectBudgets();
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || '操作失败');
    }
  }
};

const resetBudgetForm = () => {
  if (budgetFormRef.value) {
    budgetFormRef.value.resetFields();
  }
  Object.assign(budgetForm, {
    name: '',
    year: '',
    type: '',
    amount: 0,
    remark: ''
  });
};

const resetBudgetFilter = () => {
  Object.assign(budgetFilter, {
    name: '',
    year: ''
  });
  budgetPagination.current = 1;
  loadProjectBudgets();
};

// 参与人员相关方法
const showParticipantDialog = () => {
  currentParticipant.value = null;
  resetParticipantForm();
  participantDialogVisible.value = true;
};

const editParticipant = (row: any) => {
  currentParticipant.value = { ...row };
  Object.assign(participantForm, {
    staff_id: row.staff_id,
    role: row.role,
    join_date: row.join_date,
    remark: row.remark || ''
  });
  participantDialogVisible.value = true;
};

const deleteParticipant = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条参与人员记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await participantApi.deleteParticipant(row.id);
    ElMessage.success('删除成功');
    loadProjectParticipants();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const submitParticipantForm = async () => {
  if (!participantFormRef.value) return;
  
  // 检查项目是否已选择
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择项目');
    return;
  }

  try {
    const valid = await participantFormRef.value.validate();
    
    if (!valid) return;
    
    // 检查员工是否已经参与该项目 - 添加空值检查
    const existingParticipants = (participants.value || []).filter(p => p.staff_id === participantForm.staff_id);
    if (existingParticipants.length > 0 && !currentParticipant.value) {
      ElMessage.warning('该员工已经是项目参与人员');
      return;
    }
    
    if (currentParticipant.value) {
      // 更新参与人员
      await participantApi.updateParticipant(currentParticipant.value.id, participantForm);
      ElMessage.success('更新成功');
    } else {
      // 创建参与人员
      participantForm.project_id = selectedProjectId.value;
      await participantApi.createParticipant(participantForm);
      ElMessage.success('创建成功');
    }
    
    participantDialogVisible.value = false;
    // 确保这里重新加载参与人员列表
    loadProjectParticipants(); // 这一行非常重要，确保列表刷新
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || '操作失败');
    }
  }
};

const resetParticipantForm = () => {
  if (participantFormRef.value) {
    participantFormRef.value.resetFields();
  }
  Object.assign(participantForm, {
    staff_id: undefined,
    role: '',
    join_date: '',
    remark: ''
  });
};

// const resetParticipantFilter = () => {
//   Object.assign(participantFilter, {
//     staff_name: '',
//     role: ''
//   });
//   participantPagination.current = 1;
//   loadProjectParticipants();
// };

// 文档相关方法
const showDocumentDialog = () => {
  currentDocument.value = null;
  resetDocumentForm();
  documentDialogVisible.value = true;
};

const editDocument = (row: any) => {
  currentDocument.value = { ...row };
  Object.assign(documentForm, {
    name: row.name,
    file: null,
    remark: row.remark || ''
  });
  documentDialogVisible.value = true;
};

const deleteDocument = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条文档记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await documentApi.deleteProjectDocument(selectedProjectId.value, row.id);
    ElMessage.success('删除成功');
    loadProjectDocuments();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const handleFileBeforeUpload = (file: UploadRawFile) => {
  // 这里可以添加文件类型和大小的验证
  return true;
};

const handleFileChange = (file: UploadFile, fileList: UploadFile[]) => {
  if (file.raw) {
    documentForm.file = file.raw;
  }
};

const handleFileRemove = (file: UploadFile, fileList: UploadFile[]) => {
  documentForm.file = null;
};

const closeDocumentDialog = () => {
  resetDocumentForm();
  documentDialogVisible.value = false;
};

const submitDocumentForm = async () => {
  if (!documentFormRef.value) return;
  
  try {
    const valid = await documentFormRef.value.validate();
    if (!valid) return;
    
    const formData = new FormData();
    formData.append('name', documentForm.name);
    if (documentForm.file) {
      formData.append('file', documentForm.file);
    }
    formData.append('remark', documentForm.remark);
    
    if (currentDocument.value) {
      // 更新文档
      await documentApi.updateProjectDocument(selectedProjectId.value, currentDocument.value.id, formData);
      ElMessage.success('更新成功');
    } else {
      // 创建文档
      await documentApi.createProjectDocument(selectedProjectId.value, formData);
      ElMessage.success('上传成功');
    }
    
    documentDialogVisible.value = false;
    loadProjectDocuments();
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || '操作失败');
    }
  }
};

const resetDocumentForm = () => {
  if (documentFormRef.value) {
    documentFormRef.value.resetFields();
  }
  Object.assign(documentForm, {
    name: '',
    file: null,
    remark: ''
  });
  fileList.value = [];
};

const resetDocumentFilter = () => {
  Object.assign(documentFilter, {
    name: '',
    upload_date: ''
  });
  documentPagination.current = 1;
  loadProjectDocuments();
};

// 文档下载
const downloadDocument = async (filePath: string, fileName: string) => {
  try {
    // 确保filePath是完整的URL
    let url = filePath;
    if (!url.startsWith('http')) {
      // 如果不是完整URL，添加基础URL
      url = `${window.location.origin}${url}`;
    }
    
    // 下载文件
    await downloadFile(url, fileName);
  } catch (error) {
    ElMessage.error('文件下载失败');
    console.error('文件下载失败:', error);
  }
};

// 重置负责人变更筛选条件
const resetLeaderChangeFilter = () => {
  Object.assign(leaderChangeFilter, {
    change_date: ''
  });
  leaderChangePagination.current = 1;
  loadProjectLeaderChanges();
};

// 编辑项目
const handleEdit = () => {
  // 这里可以跳转到项目编辑页面或打开编辑对话框
  // 目前简单实现为跳转回项目列表
  router.push({ path: '/project', query: { edit: selectedProjectId.value } });
};

// 处理项目选择变更
const handleProjectChange = (projectId: number) => {
  if (projectId && projectId !== selectedProjectId.value) {
    selectedProjectId.value = projectId;
    // 更新URL参数，方便分享和刷新
    router.push({
      path: '/project/detail',
      query: { id: projectId }
    });
  }
};

// 返回列表
// const handleBack = () => {
//   router.push('/project');
// };

const getBudgetTypeDisplay = (type: string) => {
  // 修正：通过 .value 访问 ref 数组
  const typeMap = budgetTypeChoices.value.find(choice => choice.value === type);
  return typeMap ? typeMap.label : type;
};

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  const statusMap: Record<string, string> = {
    'APPROVED': 'success',
    'PENDING': 'warning',
    'REJECTED': 'danger',
    'IN_PROGRESS': 'primary',
    'COMPLETED': 'info'
  };
  return statusMap[status] || 'default';
};

// 格式化金额
const formatCurrency = (value: number) => {
  if (typeof value !== 'number' || isNaN(value)) {
    return '0.00';
  }
  return value.toFixed(2);
};

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (typeof bytes !== 'number' || isNaN(bytes)) {
    return '0 B';
  }
  
  if (bytes < 1024) {
    return bytes + ' B';
  } else if (bytes < 1024 * 1024) {
    return (bytes / 1024).toFixed(2) + ' KB';
  } else if (bytes < 1024 * 1024 * 1024) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  } else {
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
  }
};

// 添加loadRoleChoices函数
const loadRoleChoices = async () => {
  try {
    // 这里假设API中有获取角色列表的接口
    // 如果没有相关API，可以直接使用上面的静态数据初始化方式
    // const response = await participantApi.getRoleChoices();
    // roleChoices.value = response.data;
    
    // 使用静态数据作为替代
    roleChoices.value = [
      { label: '成员', value: 'member' },
      { label: '顾问', value: 'advisor' }
    ];
  } catch (error) {
    ElMessage.error('加载角色选项失败');
    console.error('加载角色选项失败:', error);
  }
};

// 监听项目ID变化
watch(selectedProjectId, (newId) => {
  if (newId) {
    loadProjectDetail();
    
    // 初始化时加载所有标签页数据
    loadProjectBudgets();
    loadProjectParticipants();
    loadProjectDocuments();
    loadProjectLeaderChanges();
  }
});

// 加载负责人选项
const loadLeaderOptions = async () => {
    loadingLeaders.value = true;
    try {
        const response = await staffApi.getStaffs('', undefined, undefined, '在职', 1, 1000);
        leaderOptions.value = response.data.map((staff: any) => ({
            label: staff.name,
            value: staff.id
        }));
    } catch (error) {
        ElMessage.error('加载负责人列表失败');
        console.error('Failed to load leader options:', error);
    } finally {
        loadingLeaders.value = false;
    }
};

// 显示变更负责人对话框
const showChangeLeaderDialog = async () => {
    if (!project.value) {
        ElMessage.warning('请先选择项目');
        return;
    }
    
    // 加载负责人选项
    await loadLeaderOptions();
    
    // 重置表单
    newLeaderId.value = null;
    changeRemark.value = '';
    
    // 显示对话框
    changeLeaderDialogVisible.value = true;
};

// 确认变更负责人
const confirmChangeLeader = async () => {
    if (!project.value || !newLeaderId.value) {
        ElMessage.warning('请选择新的项目负责人');
        return;
    }
    
    // 与当前负责人比较
    if (project.value.leader_id === newLeaderId.value) {
        ElMessage.warning('新负责人与当前负责人相同');
        return;
    }
    
    try {
        // 显示加载状态
        const loading = ElLoading.service({
            lock: true,
            text: '正在处理...',
            background: 'rgba(0, 0, 0, 0.7)'
        });
        
        // 调用API创建负责人变更记录
        const data = {
            project_id: project.value.id,
            leader_id: newLeaderId.value,
            change_date: new Date().toISOString().split('T')[0], // 当前日期
            remark: changeRemark.value
        };
        
        await projectApi.createProjectLeaderChange(data);
        
        // 重新加载项目信息
        await loadProjectDetail(selectedProjectId.value);
        
        // 如果当前在leaderChange标签页，重新加载变更记录
        if (activeTab.value === 'leaderChange') {
            loadProjectLeaderChanges();
        }
        
        ElMessage.success('项目负责人变更成功');
        changeLeaderDialogVisible.value = false;
    } catch (error) {
        ElMessage.error('项目负责人变更失败');
        console.error('Failed to change project leader:', error);
    } finally {
        // 关闭加载状态
        ElLoading.service().close();
    }
};

// 处理关闭变更负责人对话框
const handleCloseChangeLeaderDialog = () => {
    // 可以在这里添加清理逻辑
    changeLeaderDialogVisible.value = false;
};

// 初始化
onMounted(() => {
  loadRoleChoices(); // 取消注释并调用
  loadProjects(); // 加载项目列表
  if (selectedProjectId.value) {
    loadProjectDetail();
    loadProjectBudgets();
    loadProjectParticipants();
    loadProjectDocuments();
    loadProjectLeaderChanges();
  }
});
</script>

<style scoped>
.project-detail-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.project-info-content {
  margin-top: 20px;
}

.no-data {
  text-align: center;
  padding: 40px 0;
}

.tab-content {
  padding: 20px 0;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.budget-stats {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: bold;
}

.stat-value.income {
  color: #67c23a;
}

.stat-value.expense {
  color: #f56c6c;
}

.stat-value.tongchou {
  color: #e6a23c;
}

.stat-value.net {
  color: #409eff;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}
</style>