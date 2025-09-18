<template>
  <div class="project-detail-page">
    <!-- 项目详细信息部分 -->
    <el-card class="project-info-card">
      <template #header>
        <div class="card-header">
          <span>项目详细信息</span>
          <div class="header-actions">
            <el-button @click="handleBack">返回列表</el-button>
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
              <el-form-item label="预算名称">
                <el-input v-model="budgetFilter.name" placeholder="请输入预算名称" clearable />
              </el-form-item>
              <el-form-item label="年度">
                <el-input v-model="budgetFilter.year" placeholder="请输入年度" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="loadProjectBudgets">搜索</el-button>
                <el-button @click="resetBudgetFilter">重置</el-button>
              </el-form-item>
            </el-form>
            
            <!-- 预算统计 -->
            <div class="budget-stats" style="margin-bottom: 15px;">
              <el-row :gutter="20">
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">收入预算</span>
                    <span class="stat-value income">{{ formatCurrency(incomeBudget) }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">支出预算</span>
                    <span class="stat-value expense">{{ formatCurrency(expenseBudget) }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">统筹预算</span>
                    <span class="stat-value tongchou">{{ formatCurrency(tongchouBudget) }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <span class="stat-label">净预算</span>
                    <span class="stat-value net">{{ formatCurrency(netBudget) }}</span>
                  </div>
                </el-col>
              </el-row>
            </div>
            
            <!-- 预算表格 -->
            <el-table :data="budgets" v-loading="budgetsLoading">
              <el-table-column prop="name" label="预算名称" width="180" />
              <el-table-column prop="year" label="年度" width="100" />
              <el-table-column prop="income" label="收入(万元)" width="120" align="right">
                <template #default="{ row }">
                  {{ formatCurrency(row.income || 0) }}
                </template>
              </el-table-column>
              <el-table-column prop="expense" label="支出(万元)" width="120" align="right">
                <template #default="{ row }">
                  {{ formatCurrency(row.expense || 0) }}
                </template>
              </el-table-column>
              <el-table-column prop="tongchou" label="统筹(万元)" width="120" align="right">
                <template #default="{ row }">
                  {{ formatCurrency(row.tongchou || 0) }}
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
            <el-form :model="participantFilter" inline style="margin-bottom: 15px;">
              <el-form-item label="员工姓名">
                <el-input v-model="participantFilter.staff_name" placeholder="请输入员工姓名" clearable />
              </el-form-item>
              <el-form-item label="角色">
                <el-select v-model="participantFilter.role" placeholder="请选择角色" clearable>
                  <el-option
                    v-for="role in roleChoices"
                    :key="role.value"
                    :label="role.label"
                    :value="role.value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="loadProjectParticipants">搜索</el-button>
                <el-button @click="resetParticipantFilter">重置</el-button>
              </el-form-item>
            </el-form>
            
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
            </div>
            
            <!-- 负责人变更搜索表单 -->
            <el-form :model="leaderChangeFilter" inline style="margin-bottom: 15px;">
              <el-form-item label="变更日期">
                <el-date-picker
                  v-model="leaderChangeFilter.change_date"
                  type="date"
                  placeholder="请选择变更日期"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="loadProjectLeaderChanges">搜索</el-button>
                <el-button @click="resetLeaderChangeFilter">重置</el-button>
              </el-form-item>
            </el-form>
            
            <!-- 负责人变更表格 -->
            <el-table :data="leaderChanges" v-loading="leaderChangesLoading">
              <el-table-column prop="old_leader_name" label="原负责人" width="120" />
              <el-table-column prop="new_leader_name" label="新负责人" width="120" />
              <el-table-column prop="change_date" label="变更日期" width="150" />
              <el-table-column prop="change_reason" label="变更原因" min-width="200" />
              <el-table-column prop="operator_name" label="操作人" width="120" />
            </el-table>
            
            <!-- 负责人变更分页 -->
            <div class="pagination" style="margin-top: 15px;">
              <el-pagination
                v-model:current-page="leaderChangePagination.current"
                v-model:page-size="leaderChangePagination.size"
                :total="leaderChangePagination.total || 0"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadProjectLeaderChanges"
                @current-change="loadProjectLeaderChanges"
              />
            </div>
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
          <el-input v-model.number="budgetForm.year" placeholder="请输入年度" />
        </el-form-item>
        <el-form-item label="收入(万元)" prop="income">
          <el-input-number
            v-model.number="budgetForm.income"
            :min="0"
            :precision="2"
            :step="0.1"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="支出(万元)" prop="expense">
          <el-input-number
            v-model.number="budgetForm.expense"
            :min="0"
            :precision="2"
            :step="0.1"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="统筹(万元)" prop="tongchou">
          <el-input-number
            v-model.number="budgetForm.tongchou"
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
              :label="staff.name + '(' + staff.number + ')'"
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

// 路由和参数
const route = useRoute();
const router = useRouter();
const selectedProjectId = ref(Number(route.query.id || 0));

// 项目数据
const project = ref<Project | null>(null);
const projectLoading = ref(false);

// 活动标签页
const activeTab = ref('budget');

// 预算相关
const budgets = ref<any[]>([]);
const budgetsLoading = ref(false);
const budgetPagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const budgetFilter = reactive({
  name: '',
  year: ''
});
const budgetDialogVisible = ref(false);
const currentBudget = ref<any | null>(null);
const budgetFormRef = ref<FormInstance>();
const budgetForm = reactive({
  name: '',
  year: '',
  income: 0,
  expense: 0,
  tongchou: 0,
  remark: ''
});

// 参与人员相关
const participants = ref<any[]>([]);
const participantsLoading = ref(false);
const participantPagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const participantFilter = reactive({
  staff_name: '',
  role: ''
});
const participantDialogVisible = ref(false);
const currentParticipant = ref<any | null>(null);
const participantFormRef = ref<FormInstance>();
const participantForm = reactive({
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
  return budgets.value.reduce((sum, item) => sum + (item.income || 0), 0);
});

const expenseBudget = computed(() => {
  return budgets.value.reduce((sum, item) => sum + (item.expense || 0), 0);
});

const tongchouBudget = computed(() => {
  return budgets.value.reduce((sum, item) => sum + (item.tongchou || 0), 0);
});

const netBudget = computed(() => {
  return incomeBudget.value - expenseBudget.value - tongchouBudget.value;
});

// 表单验证规则
const budgetFormRules: FormRules = {
  name: [{ required: true, message: '请输入预算名称', trigger: 'blur' }],
  year: [{ required: true, message: '请输入年度', trigger: 'blur' }],
  income: [
    { required: true, message: '请输入收入金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '收入金额不能为负数', trigger: 'blur' }
  ],
  expense: [
    { required: true, message: '请输入支出金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '支出金额不能为负数', trigger: 'blur' }
  ],
  tongchou: [
    { required: true, message: '请输入统筹金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '统筹金额不能为负数', trigger: 'blur' }
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
    const data = await projectApi.getProjectDetail(selectedProjectId.value);
    project.value = data;
  } catch (error) {
    ElMessage.error('加载项目详情失败');
    console.error('加载项目详情失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载预算数据
const loadProjectBudgets = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    budgetsLoading.value = true;
    const params = {
      ...budgetFilter,
      page: budgetPagination.current,
      page_size: budgetPagination.size
    };
    const { results, count } = await budgetApi.getProjectBudgets(selectedProjectId.value, params);
    budgets.value = results;
    budgetPagination.total = count;
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
    const params = {
      ...participantFilter,
      page: participantPagination.current,
      page_size: participantPagination.size
    };
    const { results, count } = await participantApi.getProjectParticipants(selectedProjectId.value, params);
    participants.value = results;
    participantPagination.total = count;
  } catch (error) {
    ElMessage.error('加载参与人员数据失败');
    console.error('加载参与人员数据失败:', error);
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

// 加载角色选项
const loadRoleChoices = async () => {
  try {
    const choices = await participantApi.getRoleChoices();
    roleChoices.value = choices;
  } catch (error) {
    console.error('加载角色选项失败:', error);
  }
};

// 搜索员工
const remoteSearchStaff = async (query: string) => {
  if (!query) {
    staffOptions.value = [];
    return;
  }
  
  try {
    staffLoading.value = true;
    const staffs = await staffApi.getStaffs(query, undefined, undefined, undefined, 1, 100);
    staffOptions.value = staffs.map((staff: any) => ({
      id: staff.id,
      name: staff.name,
      number: staff.number
    }));
  } catch (error) {
    console.error('搜索员工失败:', error);
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
    name: row.name,
    year: row.year,
    income: row.income || 0,
    expense: row.expense || 0,
    tongchou: row.tongchou || 0,
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
    
    await budgetApi.deleteBudget(row.id);
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
  
  try {
    const valid = await budgetFormRef.value.validate();
    if (!valid) return;
    
    if (currentBudget.value) {
      // 更新预算
      await budgetApi.updateBudget(currentBudget.value.id, budgetForm);
      ElMessage.success('更新成功');
    } else {
      // 创建预算
      await budgetApi.createBudget(selectedProjectId.value, budgetForm);
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
    income: 0,
    expense: 0,
    tongchou: 0,
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
  
  try {
    const valid = await participantFormRef.value.validate();
    if (!valid) return;
    
    // 检查员工是否已经参与该项目
    const existingParticipants = participants.value.filter(p => p.staff_id === participantForm.staff_id);
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
      await participantApi.createParticipant(selectedProjectId.value, participantForm);
      ElMessage.success('创建成功');
    }
    
    participantDialogVisible.value = false;
    loadProjectParticipants();
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

const resetParticipantFilter = () => {
  Object.assign(participantFilter, {
    staff_name: '',
    role: ''
  });
  participantPagination.current = 1;
  loadProjectParticipants();
};

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

// 返回列表
const handleBack = () => {
  router.push('/project');
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

// 初始化
onMounted(() => {
  loadRoleChoices();
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