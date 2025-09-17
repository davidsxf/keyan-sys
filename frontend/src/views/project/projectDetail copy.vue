<template>
  <div class="project-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目详情</span>
          <div class="header-actions">
            <!-- 项目选择下拉框 -->
            <el-select
              v-model="selectedProjectId"
              placeholder="请选择项目"
              filterable
              remote
              :remote-method="remoteSearchProjects"
              :loading="projectSearchLoading"
              value-key="id"
              clearable
              @change="handleProjectChange"
              style="width: 300px; margin-right: 10px;"
            >
              <el-option
                v-for="item in projectOptions"
                :key="item.id"
                :label="`${item.number} - ${item.title}`"
                :value="item.id"
              />
            </el-select>
            <el-button-group>
              <el-button type="primary" @click="handleEdit">编辑</el-button>
              <el-button @click="handleBack">返回</el-button>
            </el-button-group>
          </div>
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

        <!-- 标签页切换 -->
        <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
          <!-- 项目经费信息 -->
          <el-tab-pane label="项目预算" name="budget">
            <el-card class="budget-card" v-loading="budgetDataLoading">
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
                  <el-col :span="4">
                    <div class="stat-item">
                      <div class="stat-label">统筹</div>
                      <div class="stat-value other">{{ tongchouBudget.toFixed(2) }}万元</div>
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
          </el-tab-pane>

          <!-- 项目参与人员 -->
          <el-tab-pane label="参与人员" name="participants">
            <el-card class="participant-card" v-loading="participantDataLoading">
              <div class="participant-header">
                <el-button type="primary" size="small" @click="showParticipantDialog">新增参与人员</el-button>
              </div>

              <!-- 参与人员表格 -->
              <el-table :data="participants" style="margin-top: 20px">
                <el-table-column prop="id" label="ID" width="80" />
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
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="{ row }">
                    <el-button size="small" @click="editParticipant(row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deleteParticipant(row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>

          <!-- 项目文档 -->
          <el-tab-pane label="项目文档" name="documents">
            <el-card class="document-card" v-loading="documentDataLoading">
              <div class="document-header">
                <el-button type="primary" size="small" @click="showDocumentDialog">新增文档</el-button>
              </div>

              <!-- 文档表格 -->
              <el-table :data="documents" style="margin-top: 20px">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="name" label="文档名称" min-width="150" />
                <!-- <el-table-column prop="file" label="文件路径" min-width="200" /> -->
                <el-table-column prop="file" label="文件" min-width="200">
                  <template #default="{ row }">
                    <el-link :href="row.file" target="_blank" @click="downloadDocument(row.file)">{{ decodeFilePath(row.file) }}</el-link>
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
                    <el-button size="small" @click="editDocument(row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deleteDocument(row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
        </el-tabs>
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
          <el-input 
            v-model.number="budgetFormData.amount" 
            placeholder="请输入金额" 
            type="number" 
            :step="0.01" 
            :precision="2"
          />
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

    <!-- 参与人员表单对话框 -->
    <el-dialog
      v-model="participantDialogVisible"
      :title="participantFormTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="participantFormRef"
        :model="participantFormData"
        :rules="participantFormRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="员工" prop="staff_id">
          <el-select 
            v-model="participantFormData.staff_id" 
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
          <el-select v-model="participantFormData.role" placeholder="请选择角色">
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
            v-model.number="participantFormData.order"
            :min="0"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="加入日期">
          <el-date-picker
            v-model="participantFormData.join_date"
            type="date"
            placeholder="请选择加入日期"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="离开日期">
          <el-date-picker
            v-model="participantFormData.leave_date"
            type="date"
            placeholder="请选择离开日期"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="participantFormData.remark"
            type="textarea"
            placeholder="请输入备注信息"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="participantDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitParticipantForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 文档表单对话框 -->
    <el-dialog
      v-model="documentDialogVisible"
      :title="documentFormTitle"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form ref="documentFormRef" :model="documentFormData" :rules="documentFormRules" label-width="80px">
        <el-form-item label="文档名称" prop="name">
          <el-input v-model="documentFormData.name" placeholder="请输入文档名称" />
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
            v-model="documentFormData.remark"
            type="textarea"
            placeholder="请输入备注信息"
            rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="documentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDocumentForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { downloadFile } from '@/utils/http';
import { Project, Choice } from '@/api/project';
import { ProjectBudget, ProjectBudgetForm } from '@/api/projectBudget';
import { ProjectStaff, ProjectStaffForm, Choice as ParticipantChoice } from '@/api/participant';
import { Staff } from '@/api/staff';
import { ProjectDocumentIn, ProjectDocumentOut } from '@/api/document';
import { projectApi } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';
import { participantApi } from '@/api/participant';
import { staffApi } from '@/api/staff';
import * as documentApi from '@/api/document';
import { API_CONFIG } from '@/config/api';

// 定义props和emit
const props = defineProps<{
  projectId?: number;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

// 当前激活的标签页
const activeTab = ref('budget');

// 项目选择相关
const selectedProjectId = ref<number>(props.projectId || 0);
const projectOptions = ref<Project[]>([]);
const projectSearchLoading = ref(false);

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

// 参与人员数据
const participants = ref<ProjectStaff[]>([]);
const participantDataLoading = ref(false);
const roleChoices = ref<ParticipantChoice[]>([]);
const participantDialogVisible = ref(false);
const participantFormRef = ref<any>(null);
const currentParticipant = ref<ProjectStaff | null>(null);
const staffs = ref<Staff[]>([]);
const staffLoading = ref(false);

// 文档数据
const documents = ref<ProjectDocumentOut[]>([]);
const file = ref<File>(null);
const documentDataLoading = ref(false);
const documentDialogVisible = ref(false);
const documentFormRef = ref<any>(null);
const currentDocument = ref<ProjectDocumentOut | null>(null);
const uploadRef = ref();

// 预算表单数据
const budgetFormData = reactive<ProjectBudgetForm>({
  project_id: 0, 
  name: '',
  amount: 0.00,
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
    { type: 'number', min: 0, message: '金额必须大于等于0', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        // 确保 value 是数字类型
        const numValue = typeof value === 'number' ? value : parseFloat(value);
        
        // 仅在新增收入预算时进行验证
        if (!currentBudget.value && budgetFormData.type === 'INCOME' && project.value.budget) {
          const newIncome = !isNaN(numValue) ? numValue : 0;
          const totalIncome = incomeBudget.value + newIncome;
          
          // 浮点数比较时考虑精度问题
          if (totalIncome > project.value.budget + 0.0001) {
            callback(new Error(`收入金额不能超过项目总预算 ${project.value.budget.toFixed(2)} 万元`));
            return;
          }
        }
        
        // 验证支出、统筹、其他不能大于结余
        if (budgetFormData.type !== 'INCOME') {
          const newAmount = !isNaN(numValue) ? numValue : 0;
          const currentAmount = currentBudget.value ? currentBudget.value.amount || 0 : 0;
          const amountDiff = newAmount - currentAmount;
          
          let totalExpense = expenseBudget.value;
          let totalTongchou = tongchouBudget.value;
          let totalOther = otherBudget.value;
          
          // 根据当前编辑的预算类型调整相应的总额
          if (currentBudget.value) {
            if (currentBudget.value.type === 'EXPENSE') {
              totalExpense -= currentAmount;
            } else if (currentBudget.value.type === 'COORDINATION') {
              totalTongchou -= currentAmount;
            } else if (currentBudget.value.type !== 'INCOME') {
              totalOther -= currentAmount;
            }
          }
          
          if (budgetFormData.type === 'EXPENSE') {
            totalExpense += newAmount;
          } else if (budgetFormData.type === 'COORDINATION') {
            totalTongchou += newAmount;
          } else if (budgetFormData.type !== 'INCOME') {
            totalOther += newAmount;
          }
          
          const totalSpending = totalExpense + totalTongchou + totalOther;
          
          if (totalSpending > incomeBudget.value + 0.0001) {
            callback(new Error(`支出、统筹、其他总额 ${totalSpending.toFixed(2)} 万元不能大于收入总额 ${incomeBudget.value.toFixed(2)} 万元`));
            return;
          }
        }
        
        callback();
      },
      trigger: 'blur'
    }
  ],
  year: [
    { required: true, message: '请输入预算年度', trigger: 'blur' },
    { type: 'number', message: '请输入有效的年份', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择预算类型', trigger: 'change' }
  ]
};

// 参与人员表单数据
const participantFormData = reactive<ProjectStaffForm>({
  project_id: 0,
  staff_id: 0,
  role: '',
  order: undefined,
  join_date: undefined,
  leave_date: undefined,
  remark: undefined
});

// 参与人员表单规则
const participantFormRules = {
  staff_id: [
    { required: true, message: '请选择员工', trigger: 'change' },
    { type: 'number', message: '员工ID必须为数字', trigger: 'change' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
};

// 文档表单数据
const documentFormData = reactive<Partial<ProjectDocumentIn>>({
  name: '',
  remark: ''
});

// 文档表单规则
const documentFormRules = {
  name: [
    { required: true, message: '请输入文档名称', trigger: 'blur' },
    { min: 1, max: 100, message: '文档名称长度应在1到100个字符之间', trigger: 'blur' }
  ],
  // file: [
  //   { required: true, message: '请选择文件', trigger: 'change' }
  // ]
};

// 表单标题计算属性
const budgetFormTitle = computed(() => {
  return currentBudget.value ? '编辑预算' : '新增预算';
});

const participantFormTitle = computed(() => {
  return currentParticipant.value ? '编辑参与人员' : '新增参与人员';
});

const documentFormTitle = computed(() => {
  return currentDocument.value ? '编辑文档' : '新增文档';
});

// 预算统计数据相关计算属性
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

const tongchouBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type === 'COORDINATION')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

const otherBudget = computed(() => {
  return budgets.value
    .filter(budget => budget.type !== 'INCOME' && budget.type !== 'EXPENSE' && budget.type !== 'COORDINATION')
    .reduce((sum, budget) => sum + (budget.amount || 0), 0);
});

const remainingBudget = computed(() => {
  return incomeBudget.value - expenseBudget.value - otherBudget.value - tongchouBudget.value;
});

// 远程搜索项目
const remoteSearchProjects = async (query: string) => {
  if (!query) {
    // 如果查询为空，加载所有项目
    await loadAllProjects();
    return;
  }
  
  projectSearchLoading.value = true;
  try {
    const response = await projectApi.getProjects({ title: query });
    projectOptions.value = response.items || [];
  } catch (error) {
    ElMessage.error('搜索项目失败');
    console.error('搜索项目失败:', error);
  } finally {
    projectSearchLoading.value = false;
  }
};

// 加载所有项目
const loadAllProjects = async () => {
  projectSearchLoading.value = true;
  try {
    const response = await projectApi.getProjects({});
    projectOptions.value = response.items || [];
  } catch (error) {
    ElMessage.error('加载项目列表失败');
    console.error('加载项目列表失败:', error);
  } finally {
    projectSearchLoading.value = false;
  }
};

// 处理项目选择变化
const handleProjectChange = async (projectId: number) => {
  if (!projectId) {
    // 如果清空选择，清空所有数据
    project.value = {} as Project;
    budgets.value = [];
    participants.value = [];
    documents.value = [];
    return;
  }
  
  // 加载选中项目的详情
  projectLoading.value = true;
  try {
    project.value = await projectApi.getProject(projectId);
    // 加载项目的预算数据
    loadProjectBudgets();
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载项目详情
const loadProjectDetail = async () => {
  if (!selectedProjectId.value) return;
  
  projectLoading.value = true;
  try {
    project.value = await projectApi.getProject(selectedProjectId.value);
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  } finally {
    projectLoading.value = false;
  }
};

// 加载项目预算列表
const loadProjectBudgets = async () => {
  if (!selectedProjectId.value) return;
  
  budgetDataLoading.value = true;
  try {
    const response = await projectBudgetApi.getProjectBudgets({ project_id: selectedProjectId.value });
    budgets.value = response.items;
  } catch (error) {
    ElMessage.error('获取预算列表失败');
    console.error('获取预算列表失败:', error);
  } finally {
    budgetDataLoading.value = false;
  }
};

// 加载项目参与人员列表
const loadProjectParticipants = async () => {
  if (!selectedProjectId.value) return;
  
  participantDataLoading.value = true;
  try {
    const response = await participantApi.getProjectParticipants(selectedProjectId.value);
    participants.value = response.items;
  } catch (error) {
    ElMessage.error('获取参与人员列表失败');
    console.error('获取参与人员列表失败:', error);
  } finally {
    participantDataLoading.value = false;
  }
};

// 加载项目文档列表
const loadProjectDocuments = async () => {
  if (!selectedProjectId.value) return;
  
  documentDataLoading.value = true;
  try {
    const response = await documentApi.getProjectDocuments(selectedProjectId.value, {});
    documents.value = response.items || [];
  } catch (error) {
    ElMessage.error('获取文档列表失败');
    console.error('获取文档列表失败:', error);
  } finally {
    documentDataLoading.value = false;
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

// 加载角色选项
const loadRoleChoices = async () => {
  try {
    roleChoices.value = await participantApi.getParticipantRoles();
  } catch (error) {
    ElMessage.error('获取角色选项失败');
    console.error('获取角色选项失败:', error);
  }
};

// 加载所有员工
const loadAllStaffs = async () => {
  staffLoading.value = true;
  try {
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

// 标签页点击事件处理
const handleTabClick = (tab: any) => {
  const tabName = tab?.props?.name; // 增加可选链操作符
  if (tabName === 'budget' && (!budgets.value || budgets.value.length === 0)) {
    loadProjectBudgets();
  } else if (tabName === 'participants' && (!participants.value || participants.value.length === 0)) {
    loadProjectParticipants();
  } else if (tabName === 'documents' && (!documents.value || documents.value.length === 0)) {
    loadProjectDocuments();
  }
};

// 显示预算对话框
const showBudgetDialog = () => {
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择项目');
    return;
  }
  
  currentBudget.value = null;
  budgetFormData.project_id = selectedProjectId.value;
  budgetFormData.name = '';
  budgetFormData.amount = 0.00;
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
  budgetFormData.amount = budget.amount || 0.00;
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

// 显示参与人员对话框
const showParticipantDialog = () => {
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择项目');
    return;
  }
  
  currentParticipant.value = null;
  participantFormData.project_id = selectedProjectId.value;
  participantFormData.staff_id = 0;
  participantFormData.role = '';
  participantFormData.order = undefined;
  participantFormData.join_date = undefined;
  participantFormData.leave_date = undefined;
  participantFormData.remark = undefined;
  participantDialogVisible.value = true;
};

// 编辑参与人员
const editParticipant = (participant: ProjectStaff) => {
  currentParticipant.value = participant;
  // 填充表单数据
  participantFormData.project_id = participant.project_id;
  participantFormData.staff_id = participant.staff_id;
  participantFormData.role = participant.role;
  participantFormData.order = participant.order;
  participantFormData.join_date = participant.join_date;
  participantFormData.leave_date = participant.leave_date;
  participantFormData.remark = participant.remark;
  participantDialogVisible.value = true;
};

// 删除参与人员
const deleteParticipant = async (participant: ProjectStaff) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除参与人员「${participant.staff_name}」吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    await participantApi.deleteParticipant(participant.id);
    ElMessage.success('删除成功');
    loadProjectParticipants();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除参与人员失败:', error);
    }
  }
};

// 提交参与人员表单
const submitParticipantForm = async () => {
  if (!participantFormRef.value) return;
  
  try {
    await participantFormRef.value.validate();
    
    // 检查是否是编辑操作且修改了员工
    const isEditingDifferentStaff = currentParticipant.value && 
      participantFormData.staff_id !== currentParticipant.value.staff_id;
    
    // 新增操作或编辑时修改了员工，需要检查重复
    if (!currentParticipant.value || isEditingDifferentStaff) {
      // 检查员工是否已参与该项目
      const isParticipated = participants.value.some(
        item => item.staff_id === participantFormData.staff_id &&
                // 排除当前正在编辑的记录
                (!currentParticipant.value || item.id !== currentParticipant.value.id)
      );
      
      if (isParticipated) {
        ElMessage.error('该员工已参与此项目');
        return;
      }
    }
    
    // 创建一个新对象，用于提交，避免修改原始formData
    const submitData = { ...participantFormData };
    
    // 格式化日期字段为ISO字符串格式 (YYYY-MM-DD)
    if (submitData.join_date) {
      submitData.join_date = new Date(submitData.join_date).toISOString().split('T')[0];
    }
    if (submitData.leave_date) {
      submitData.leave_date = new Date(submitData.leave_date).toISOString().split('T')[0];
    }
    
    if (currentParticipant.value) {
      // 更新参与人员
      await participantApi.updateParticipant(currentParticipant.value.id, submitData);
      ElMessage.success('参与人员更新成功');
    } else {
      // 创建参与人员
      await participantApi.createParticipant(submitData);
      ElMessage.success('参与人员创建成功');
    }
    
    participantDialogVisible.value = false;
    loadProjectParticipants();
  } catch (error) {
    const axiosError = error as any;
    const errorMessage = axiosError.response?.data?.detail || axiosError.message || '操作失败';
    
    // 处理后端返回的"该员工已参与此项目"错误
    if (errorMessage.includes('该员工已参与此项目')) {
      ElMessage.error('该员工已参与此项目');
    } else {
      // 只记录错误但不显示给用户
      console.error('提交表单失败:', errorMessage);
    }
  }
};


// 显示文档对话框
const showDocumentDialog = () => {
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择项目');
    return;
  }
  
  currentDocument.value = null;
  documentFormData.name = '';
  // documentFormData.file = null;
  // file 上传文件
  file.value = null;
  documentFormData.remark = '';
  
  if (documentFormRef.value) {
    documentFormRef.value.resetFields();
  }
  
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
  
  documentDialogVisible.value = true;
};

// 编辑文档
const editDocument = (document: ProjectDocumentOut) => {
  currentDocument.value = document;
  // 填充表单数据
  documentFormData.name = document.name;
  documentFormData.remark = document.remark || '';
  documentDialogVisible.value = true;
};

// 删除文档
const deleteDocument = async (document: ProjectDocumentOut) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文档「${document.name}」吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    // 修正参数数量，只传递document.id
    await documentApi.deleteProjectDocument(document.id);
    ElMessage.success('删除成功');
    loadProjectDocuments();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error('删除文档失败:', error);
    }
  }
};

// 处理文件选择
const handleFileChange = (uploadFile: any) => {
  file.value = uploadFile.raw;
  
};

// 提交文档表单
const submitDocumentForm = async () => {
  if (!file.value) {
    ElMessage.warning('请选择文件');
    return;
  }
  
  try {
    await documentFormRef.value.validate();
    
    console.log('submitDocumentForm', selectedProjectId.value, documentFormData);
    
    if (currentDocument.value) {
      // 更新文档
      // await documentApi.updateProjectDocument(currentDocument.value.id, documentFormData);
      ElMessage.success('文档更新成功');
    } else {
      // 创建文档 - 传递正确的 file.value
      console.log('handleFileChange', file.value);
      await documentApi.createProjectDocument(selectedProjectId.value, documentFormData, file.value);
      ElMessage.success('文档创建成功');
    }
    
    documentDialogVisible.value = false;
    loadProjectDocuments();
  } catch (error) {
    console.error('提交表单失败:', error);
    // 尝试获取更具体的错误信息
    const axiosError = error as any;
    const errorMessage = axiosError.response?.data?.error || 
                        axiosError.response?.data?.detail || 
                        axiosError.message || 
                        (currentDocument.value ? '文档更新失败' : '文档创建失败');
    
    ElMessage.error(errorMessage);
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


// 修改下载函数实现
const downloadDocument = async (filePath: string) => {
  try {
    // 组合完整的文件URL
    let fullUrl = filePath;
    
    // 检查filePath是否是完整URL，如果不是则添加后端API域名
    if (!fullUrl.startsWith('http')) {
      // 确保路径以/开头
      if (!fullUrl.startsWith('/')) {
        fullUrl = '/' + fullUrl;
      }
      // 添加后端API域名
      fullUrl = window.location.origin + fullUrl;
    }
    
    // 获取文件名并解码中文字符
    let filename = filePath.split('/').pop() || 'document';
    try {
      // 尝试解码文件名中的中文字符
      filename = decodeURIComponent(filename);
    } catch (e) {
      // 如果解码失败则使用原始文件名
      console.warn('文件名解码失败，使用原始文件名');
    }
    
    // 调用专门的下载函数
    await downloadFile(fullUrl, filename);
  } catch (error) {
    console.error('下载文件失败:', error);
    // 添加错误提示
    ElMessage.error('文件下载失败，请稍后重试');
  }
};

// 在 script 标签中的响应式数据定义后添加解码函数
const decodeFilePath = (filePath: string): string => {
  try {
    // 尝试解码 URL 编码的中文字符
    return decodeURIComponent(filePath);
  } catch (e) {
    // 如果解码失败，则返回原始路径
    return filePath;
  }
};

// 编辑项目
const handleEdit = () => {
  if (!selectedProjectId.value) {
    ElMessage.warning('请先选择项目');
    return;
  }
  // 使用emit或其他方式处理编辑导航
  console.log('编辑项目:', selectedProjectId.value);
};

// 返回上一页（在对话框中改为关闭）
const handleBack = () => {
  emit('close');
};

// 监听selectedProjectId变化，重新加载数据
watch(
  () => selectedProjectId.value,
  (newId) => {
    if (newId) {
      loadProjectDetail();
      // 默认加载预算数据
      loadProjectBudgets();
      loadProjectDocuments();
    }
  },
  { immediate: true }
);

// 初始化数据
onMounted(() => {
  loadAllProjects();
  loadBudgetTypeChoices();
  loadRoleChoices();
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

.header-actions {
  display: flex;
  align-items: center;
}

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card,
.budget-card,
.participant-card,
.document-card {
  background-color: #fff;
}

.budget-header,
.participant-header,
.document-header {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>