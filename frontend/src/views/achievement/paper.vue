<template>
  <div class="container">
    <div class="header">
      <el-page-header
        :icon="Back"
        content="文献管理"
        @back="handleBack"
      />
      <div class="actions">
        <el-input
          v-model="searchForm.title"
          placeholder="请输入文献标题"
          clearable
          class="search-input"
          @blur="handleSearch"
          @clear="handleSearch"
        />
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新增文献
        </el-button>
      </div>
    </div>

    <el-card class="content-card">
      <el-table
        v-loading="loading"
        :data="paperList"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="文献标题" min-width="300" show-overflow-tooltip />
        <el-table-column prop="journal" label="发表期刊" min-width="200">
          <template #default="scope">
            {{ scope.row.journal?.name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="publication_year" label="发表年份" width="120" />
        <el-table-column label="第一作者" min-width="150">
          <template #default="scope">
            <span v-if="scope.row.first_authors && scope.row.first_authors.length > 0">
              {{ scope.row.first_authors.map(author => author.name).join('; ') }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="通讯作者" min-width="150">
          <template #default="scope">
            <span v-if="scope.row.corresponding_authors && scope.row.corresponding_authors.length > 0">
              {{ scope.row.corresponding_authors.map(author => author.name).join('; ') }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="unit_ranking" label="单位排名" width="100" />
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

    <!-- 文献编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="文献标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入文献标题"
            clearable
            type="textarea"
            rows="2"
          />
        </el-form-item>
        
        <!-- 期刊选择 -->
        <el-form-item label="发表期刊" prop="journal_id">
          <el-select
            v-model="formData.journal_id"
            placeholder="请选择发表期刊"
            clearable
            filterable
            @change="handleJournalChange"
          >
            <el-option
              v-for="journal in journalOptions"
              :key="journal.id"
              :label="journal.name"
              :value="journal.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 期刊详情信息 -->
        <template v-if="selectedJournal">
          <el-form-item label="期刊信息">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="ISSN">{{ selectedJournal.issn }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatDate(selectedJournal.created_at) }}</el-descriptions-item>
            </el-descriptions>
          </el-form-item>
          
          <!-- JCR分区和影响因子输入 -->
          <el-form-item label="当年JCR分区" prop="jcr_quartile">
            <el-radio-group v-model="formData.jcr_quartile">
              <el-radio-button label="Q1">Q1</el-radio-button>
              <el-radio-button label="Q2">Q2</el-radio-button>
              <el-radio-button label="Q3">Q3</el-radio-button>
              <el-radio-button label="Q4">Q4</el-radio-button>
              <el-radio-button label="undefined">未分区</el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="当年影响因子" prop="impact_factor">
            <el-input
              v-model.number="formData.impact_factor"
              placeholder="请输入影响因子"
              clearable
              type="number"
              :min="0"
              :step="0.001"
            />
          </el-form-item>
        </template>
        
        <el-form-item label="发表年份" prop="publication_year">
          <el-input
            v-model.number="formData.publication_year"
            placeholder="请输入发表年份"
            clearable
            type="number"
            :min="1900"
            :max="new Date().getFullYear()+1"
          />
        </el-form-item>
        
        <el-form-item label="单位排名" prop="unit_ranking">
          <el-input
            v-model="formData.unit_ranking"
            placeholder="请输入单位排名"
            clearable
            type="number"
            :min="1"
          />
        </el-form-item>
        
        <el-form-item label="页码" prop="page_numbers">
          <el-input
            v-model="formData.page_numbers"
            placeholder="请输入页码范围"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="关键词" prop="keywords">
          <el-input
            v-model="formData.keywords"
            placeholder="请输入关键词，多个关键词用分号分隔"
            clearable
            type="textarea"
            rows="2"
          />
        </el-form-item>
        
        <el-form-item label="摘要" prop="abstract">
          <el-input
            v-model="formData.abstract"
            placeholder="请输入摘要"
            clearable
            type="textarea"
            rows="4"
          />
        </el-form-item>
        
        <!-- 作者选择 -->
        <el-form-item label="第一作者" prop="first_author_ids">
          <el-select
            v-model="formData.first_author_ids"
            placeholder="请选择第一作者"
            multiple
            filterable
            collapse-tags
            style="width: 100%"
          >
            <el-option
              v-for="author in authorOptions"
              :key="author.id"
              :label="author.name"
              :value="author.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="通讯作者" prop="corresponding_author_ids">
          <el-select
            v-model="formData.corresponding_author_ids"
            placeholder="请选择通讯作者"
            multiple
            filterable
            collapse-tags
            style="width: 100%"
          >
            <el-option
              v-for="author in authorOptions"
              :key="author.id"
              :label="author.name"
              :value="author.id"
            />
          </el-select>
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
import type { Paper, PaperForm, Journal, Author } from '@/api/achievement';

// 路由
const router = useRouter();

// 状态
const loading = ref(false);
const dialogVisible = ref(false);
const dialogTitle = ref('');
const formRef = ref<FormInstance>();

// 文献列表
const paperList = ref<Paper[]>([]);

// 搜索表单
const searchForm = reactive({
  title: ''
});

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 期刊选项
const journalOptions = ref<Array<{ id: number; name: string; issn: string; created_at: string }>>([]);
const selectedJournal = ref<Journal | null>(null);

// 作者选项
const authorOptions = ref<Array<{ id: number; name: string }>>([]);

// 表单数据 - 扩展PaperForm接口以包含期刊指标
interface ExtendedPaperForm extends PaperForm {
  jcr_quartile?: string;
  impact_factor?: number;
}

const formData = reactive<ExtendedPaperForm>({
  title: '',
  first_author_ids: [],
  corresponding_author_ids: [],
  journal_id: undefined,
  publication_year: new Date().getFullYear(),
  unit_ranking: 1,
  page_numbers: '',
  keywords: '',
  abstract: '',
  jcr_quartile: undefined,
  impact_factor: undefined
});

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入文献标题', trigger: 'blur' },
    { min: 1, max: 500, message: '文献标题长度在1-500个字符之间', trigger: 'blur' }
  ],
  journal_id: [
    { required: true, message: '请选择发表期刊', trigger: 'change' }
  ],
  publication_year: [
    { required: true, message: '请输入发表年份', trigger: 'blur' },
    { type: 'number', min: 1900, message: '发表年份不能早于1900年', trigger: 'blur' },
    { type: 'number', max: new Date().getFullYear()+1, message: '发表年份不能超过明年', trigger: 'blur' }
  ],
  unit_ranking: [
    { required: true, message: '请输入单位排名', trigger: 'blur' },
    { type: 'number', min: 1, message: '单位排名必须大于0', trigger: 'blur' }
  ],
  first_author_ids: [
    { required: true, message: '请至少选择一位第一作者', trigger: 'change' },
    { type: 'array', min: 1, message: '请至少选择一位第一作者', trigger: 'change' }
  ],
  corresponding_author_ids: [
    { required: true, message: '请至少选择一位通讯作者', trigger: 'change' },
    { type: 'array', min: 1, message: '请至少选择一位通讯作者', trigger: 'change' }
  ],
  jcr_quartile: [
    { required: true, message: '请选择JCR分区', trigger: 'change' }
  ],
  impact_factor: [
    { required: true, message: '请输入影响因子', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        // 确保值是数字类型并且大于等于0
        if (value === undefined || value === null || isNaN(Number(value)) || Number(value) < 0) {
          callback(new Error('影响因子必须大于等于0'));
        } else {
          callback();
        }
      },
      trigger: 'blur,change'
    }
  ]
};

// 当前编辑的文献ID
let currentPaperId: number | null = null;

/**
 * 格式化日期
 * @param dateString 日期字符串
 * @returns 格式化后的日期
 */
const formatDate = (dateString?: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};

/**
 * 加载期刊选项列表
 * 用于文献编辑时选择期刊
 */
const loadJournalOptions = async () => {
  try {
    const response = await achievementApi.getJournals();
    journalOptions.value = response.map(journal => ({
      id: journal.id,
      name: journal.name,
      issn: journal.issn,
      created_at: journal.created_at
    }));
  } catch (error) {
    console.error('获取期刊选项失败:', error);
    ElMessage.error('获取期刊选项失败');
  }
};

/**
 * 加载作者选项列表
 * 用于文献编辑时选择作者
 */
const loadAuthorOptions = async () => {
  try {
    // 调用作者API获取作者列表，设置较大的limit以获取完整列表
    const response = await achievementApi.getAuthors({ limit: 1000 });
    authorOptions.value = response.map(author => ({ id: author.id, name: author.name }));
  } catch (error) {
    console.error('获取作者选项失败:', error);
    ElMessage.error('获取作者选项失败');
  }
};

/**
 * 加载文献列表
 * 支持搜索和分页
 */
const loadPapers = async () => {
  loading.value = true;
  try {
    // 调用文献API获取列表
    // 注意：当前API没有实现分页和过滤，实际项目中应根据后端API设计调整
    const response = await achievementApi.getPapers();
    
    // 应用搜索过滤
    let filteredPapers = response;
    if (searchForm.title && searchForm.title.trim()) {
      const searchTerm = searchForm.title.trim().toLowerCase();
      filteredPapers = response.filter(paper => 
        paper.title.toLowerCase().includes(searchTerm)
      );
    }
    
    // 应用分页
    const startIndex = (pagination.currentPage - 1) * pagination.pageSize;
    const endIndex = startIndex + pagination.pageSize;
    
    paperList.value = filteredPapers.slice(startIndex, endIndex);
    pagination.total = filteredPapers.length;
  } catch (error) {
    console.error('获取文献列表失败:', error);
    ElMessage.error('获取文献列表失败');
  } finally {
    loading.value = false;
  }
};

/**
 * 期刊选择变化处理
 * 当用户选择期刊后，显示JCR分区和影响因子输入区域
 * @param journalId 选中的期刊ID
 */
const handleJournalChange = async (journalId?: number) => {
  if (!journalId) {
    selectedJournal.value = null;
    formData.jcr_quartile = undefined;
    formData.impact_factor = undefined;
    return;
  }
  
  try {
    // 获取期刊详情
    const journal = await achievementApi.getJournal(journalId);
    selectedJournal.value = journal;
    
    // 如果期刊有默认的JCR分区和影响因子，可以预先填充
    if (journal.jcr_quartile) {
      formData.jcr_quartile = journal.jcr_quartile;
    }
    if (journal.impact_factor !== undefined) {
      formData.impact_factor = journal.impact_factor;
    }
  } catch (error) {
    console.error('获取期刊详情失败:', error);
    ElMessage.error('获取期刊详情失败');
  }
};

/**
 * 重置表单数据
 */
const resetForm = () => {
  formRef.value?.resetFields();
  Object.assign(formData, {
    title: '',
    first_author_ids: [],
    corresponding_author_ids: [],
    journal_id: undefined,
    publication_year: new Date().getFullYear(),
    unit_ranking: 1,
    page_numbers: '',
    keywords: '',
    abstract: '',
    jcr_quartile: undefined,
    impact_factor: undefined
  });
  selectedJournal.value = null;
  currentPaperId = null;
};

/**
 * 处理新增文献
 */
const handleCreate = () => {
  dialogTitle.value = '新增文献';
  resetForm();
  dialogVisible.value = true;
};

/**
 * 处理编辑文献
 * @param paper 要编辑的文献对象
 */
const handleEdit = async (paper: Paper) => {
  dialogTitle.value = '编辑文献';
  currentPaperId = paper.id;
  
  // 填充表单数据
  Object.assign(formData, {
    title: paper.title,
    first_author_ids: paper.first_authors?.map(author => author.id) || [],
    corresponding_author_ids: paper.corresponding_authors?.map(author => author.id) || [],
    journal_id: paper.journal?.id,
    publication_year: paper.publication_year,
    unit_ranking: paper.unit_ranking,
    page_numbers: paper.page_numbers || '',
    keywords: paper.keywords || '',
    abstract: paper.abstract || ''
  });
  
  // 如果有期刊信息，加载期刊详情
  if (paper.journal?.id) {
    await handleJournalChange(paper.journal.id);
  }
  
  dialogVisible.value = true;
};

/**
 * 处理删除文献
 * @param id 文献ID
 */
const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文献吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    // 调用API删除文献
    await achievementApi.deletePaper(id);
    ElMessage.success('删除成功');
    // 重新加载列表
    await loadPapers();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文献失败:', error);
      // 如果是API返回的错误信息，尝试提取显示
      if (error.response?.data?.detail) {
        ElMessage.error(error.response.data.detail);
      } else {
        ElMessage.error('删除失败');
      }
    }
  }
};

/**
 * 保存期刊年度指标
 * @param journalId 期刊ID
 * @param year 年份
 * @param jcrQuartile JCR分区
 * @param impactFactor 影响因子
 */
const saveJournalMetric = async (journalId: number, year: number, jcrQuartile?: string, impactFactor?: number) => {
  try {
    // 构建期刊指标数据
    const metricData = {
      year,
      jcr_quartile: jcrQuartile || '',
      impact_factor: impactFactor || null
    };
    
    // 尝试获取该年份的现有指标
    try {
      // 检查是否已存在该年份的指标
      await achievementApi.getJournalMetricByYear(journalId, year);
      // 如果存在，则更新
      await achievementApi.updateJournalMetric(journalId, year, metricData);
    } catch (error) {
      // 如果不存在（通常是404错误），则创建新的指标
      await achievementApi.createJournalMetric(journalId, metricData);
    }
  } catch (error) {
    console.error('保存期刊年度指标失败:', error);
    // 不抛出错误，因为即使期刊指标保存失败，论文仍应继续保存
    ElMessage.warning('论文已保存，但期刊指标保存失败');
  }
};

/**
 * 处理表单提交
 * 根据是否有currentPaperId决定是创建还是更新
 */
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    // 准备提交数据，合并期刊指标信息
    const submitData = {
      ...formData
    };
    
    if (currentPaperId) {
      // 更新文献
      await achievementApi.updatePaper(currentPaperId, submitData);
      ElMessage.success('更新成功');
    } else {
      // 创建新文献
      await achievementApi.createPaper(submitData);
      ElMessage.success('创建成功');
    }
    
    // 保存期刊年度指标（如果有期刊和发表年份）
    if (formData.journal_id && formData.publication_year) {
      await saveJournalMetric(
        formData.journal_id, 
        formData.publication_year, 
        formData.jcr_quartile, 
        formData.impact_factor
      );
    }
    
    dialogVisible.value = false;
    // 重新加载列表
    await loadPapers();
  } catch (error: any) {
    console.error('保存文献失败:', error);
    // 如果是API返回的错误信息，尝试提取显示
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail);
    } else {
      ElMessage.error(currentPaperId ? '更新失败' : '创建失败');
    }
  }
};

/**
 * 处理搜索
 * 在输入框失去焦点时触发搜索
 */
const handleSearch = () => {
  // 重置为第一页
  pagination.currentPage = 1;
  // 调用加载文献列表函数
  loadPapers();
};

/**
 * 处理分页大小变化
 * @param size 新的每页数量
 */
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadPapers();
};

/**
 * 处理当前页变化
 * @param current 新的当前页码
 */
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadPapers();
};

/**
 * 处理返回
 */
const handleBack = () => {
  router.back();
};

// 初始化 - 并发加载所有必要数据
onMounted(async () => {
  try {
    await Promise.all([
      loadJournalOptions(),
      loadAuthorOptions(),
      loadPapers()
    ]);
  } catch (error) {
    console.error('初始化数据加载失败:', error);
  }
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
  width: 400px;
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