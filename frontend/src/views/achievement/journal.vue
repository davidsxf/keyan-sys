<template>
  <div class="container mx-auto py-4">
    <div class="card">
      <div class="card-header flex justify-between items-center">
        <h2 class="text-xl font-bold">期刊管理</h2>
        <el-button type="primary" @click="handleAddJournal">
          <el-icon><Plus /></el-icon>
          添加期刊
        </el-button>
      </div>
      
      <!-- 搜索表单 -->
      <div class="card-body bg-gray-50 p-4">
        <el-form ref="searchForm" :model="searchForm" layout="inline" size="small">
          <el-form-item label="刊名">
            <el-input v-model="searchForm.name" placeholder="请输入刊名" clearable style="width: 200px" />
          </el-form-item>
          <el-form-item label="ISSN">
            <el-input v-model="searchForm.issn" placeholder="请输入ISSN" clearable style="width: 150px" />
          </el-form-item>
          <el-form-item label="JCR分区">
            <el-select v-model="searchForm.jcr_quartile" placeholder="请选择JCR分区" clearable style="width: 150px">
              <el-option label="Q1" value="Q1" />
              <el-option label="Q2" value="Q2" />
              <el-option label="Q3" value="Q3" />
              <el-option label="Q4" value="Q4" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 期刊列表 -->
      <div class="card-body">
        <el-table v-loading="loading" :data="journals" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="刊名" show-overflow-tooltip />
          <el-table-column prop="issn" label="ISSN" width="120" />
          <el-table-column prop="jcr_quartile" label="JCR分区" width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.jcr_quartile" :type="getQuartileType(scope.row.jcr_quartile)">
                {{ scope.row.jcr_quartile }}
              </el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="impact_factor" label="影响因子" width="120">
            <template #default="scope">
              {{ scope.row.impact_factor || '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEditJournal(scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteJournal(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="flex justify-between items-center mt-4">
          <div class="text-sm text-gray-500">
            共 {{ total }} 条数据
          </div>
          <el-pagination
            v-model:current-page="pagination.currentPage"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>

    <!-- 添加/编辑期刊对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" @close="handleDialogClose">
      <el-form ref="journalFormRef" :model="journalForm" :rules="journalRules" label-width="120px">
        <el-form-item label="刊名" prop="name">
          <el-input v-model="journalForm.name" placeholder="请输入刊名" />
        </el-form-item>
        <el-form-item label="ISSN" prop="issn">
          <el-input v-model="journalForm.issn" placeholder="请输入ISSN" />
        </el-form-item>
        <el-form-item label="JCR分区" prop="jcr_quartile">
          <el-select v-model="journalForm.jcr_quartile" placeholder="请选择JCR分区" clearable>
            <el-option label="Q1" value="Q1" />
            <el-option label="Q2" value="Q2" />
            <el-option label="Q3" value="Q3" />
            <el-option label="Q4" value="Q4" />
          </el-select>
        </el-form-item>
        <el-form-item label="影响因子" prop="impact_factor">
          <el-input v-model.number="journalForm.impact_factor" type="number" placeholder="请输入影响因子" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog v-model="deleteDialogVisible" title="确认删除" width="400px">
      <p>确定要删除该期刊吗？</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="handleConfirmDelete">确定删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElForm } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import { achievementApi } from '@/api/achievement';
import type { Journal, JournalForm, JournalFilter } from '@/api/achievement';

// 期刊列表数据
const journals = ref<Journal[]>([]);
const loading = ref(false);
const total = ref(0);

// 搜索表单
const searchForm = reactive<JournalFilter>({});

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10
});

// 对话框状态
const dialogVisible = ref(false);
const deleteDialogVisible = ref(false);
const currentJournalId = ref<number | null>(null);
const dialogTitle = computed(() => currentJournalId.value ? '编辑期刊' : '添加期刊');

// 期刊表单数据
const journalForm = reactive<JournalForm>({
  name: '',
  issn: '',
  jcr_quartile: undefined,
  impact_factor: undefined
});

// 表单验证规则
const journalRules = {
  name: [
    { required: true, message: '请输入刊名', trigger: 'blur' },
    { max: 200, message: '刊名不能超过200个字符', trigger: 'blur' }
  ],
  issn: [
    { required: true, message: '请输入ISSN', trigger: 'blur' },
    { max: 20, message: 'ISSN不能超过20个字符', trigger: 'blur' }
  ]
};

// 获取期刊列表
const loadJournals = async () => {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize
    };
    const response = await achievementApi.getJournals(params);
    journals.value = response;
    // 由于后端没有返回总数，这里暂时使用列表长度作为总数
    // 实际项目中应该从后端获取真实的总数
    total.value = response.length;
  } catch (error) {
    ElMessage.error('获取期刊列表失败');
    console.error('获取期刊列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 获取JCR分区对应的标签类型
const getQuartileType = (quartile: string) => {
  const typeMap: Record<string, string> = {
    'Q1': 'primary',
    'Q2': 'success',
    'Q3': 'warning',
    'Q4': 'info'
  };
  return typeMap[quartile] || 'default';
};

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1;
  loadJournals();
};

// 重置搜索表单
const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    delete searchForm[key as keyof JournalFilter];
  });
  pagination.currentPage = 1;
  loadJournals();
};

// 分页大小变更
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadJournals();
};

// 当前页变更
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadJournals();
};

// 添加期刊
const handleAddJournal = () => {
  currentJournalId.value = null;
  // 重置表单 - 正确设置字段类型
  journalForm.name = '';
  journalForm.issn = '';
  journalForm.jcr_quartile = undefined;
  journalForm.impact_factor = undefined;
  // 重置表单验证状态
  if (journalFormRef.value) {
    journalFormRef.value.resetFields();
  }
  dialogVisible.value = true;
};

// 编辑期刊
const handleEditJournal = async (journal: Journal) => {
  currentJournalId.value = journal.id;
  // 填充表单数据
  Object.assign(journalForm, journal);
  dialogVisible.value = true;
};

// 删除期刊
const handleDeleteJournal = (id: number) => {
  currentJournalId.value = id;
  deleteDialogVisible.value = true;
};

// 确认删除
const handleConfirmDelete = async () => {
  if (!currentJournalId.value) return;
  
  try {
    await achievementApi.deleteJournal(currentJournalId.value);
    ElMessage.success('期刊删除成功');
    deleteDialogVisible.value = false;
    loadJournals();
  } catch (error) {
    // 处理特定错误消息
    const errorMessage = error instanceof Error ? error.message : '期刊删除失败';
    ElMessage.error(errorMessage);
    console.error('删除期刊失败:', error);
  }
};

// 添加表单引用
const journalFormRef = ref<InstanceType<typeof ElForm>>();

// 提交表单
const handleSubmit = async () => {
  // 先进行表单验证
  try {
    const isValid = await journalFormRef.value?.validate();
    if (!isValid) return;
  } catch (error) {
    return; // 验证失败，直接返回
  }
  
  try {
    if (currentJournalId.value) {
      // 更新期刊
      await achievementApi.updateJournal(currentJournalId.value, journalForm);
      ElMessage.success('期刊更新成功');
    } else {
      // 添加期刊
      await achievementApi.createJournal(journalForm);
      ElMessage.success('期刊添加成功');
    }
    dialogVisible.value = false;
    loadJournals();
  } catch (error) {
    // 处理特定错误消息
    const errorMessage = error instanceof Error ? error.message : currentJournalId.value ? '期刊更新失败' : '期刊添加失败';
    ElMessage.error(errorMessage);
    console.error(currentJournalId.value ? '更新期刊失败:' : '添加期刊失败:', error);
  }
};

// 对话框关闭处理
const handleDialogClose = () => {
  // 重置表单 - 正确设置字段类型
  journalForm.name = '';
  journalForm.issn = '';
  journalForm.jcr_quartile = undefined;
  journalForm.impact_factor = undefined;
  // 重置表单验证状态
  if (journalFormRef.value) {
    journalFormRef.value.resetFields();
  }
};

// 初始化加载数据
onMounted(() => {
  loadJournals();
});
</script>

<style scoped>
.container {
  width: 100%;
  padding: 0 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.card-body {
  padding: 20px;
}
</style>