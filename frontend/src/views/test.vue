<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElTable, ElTableColumn, ElDialog, ElButton, ElForm, ElFormItem, ElInput, ElInputNumber } from 'element-plus';
import { getCategories, createCategory, updateCategory, deleteCategory } from '@/api/category';

// 使用category.ts中定义的Category类型
import type { Category } from '@/api/category';

// 定义响应式变量
const listData = ref<Category[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const dialogType = ref('create'); // create or edit
const currentCategory = reactive<Category>({
  id: undefined,
  name: '',
  parent: null,
  weight: 0,
  sort_order: 0
});
const formRef = ref();

// 调用后端API获取列表数据
const fetchListData = async () => {
  loading.value = true;
  try {
    const data = await getCategories();
    // console.log('API响应数据:', data.data);
    
    if (data && data.success ) {
      listData.value = data.data;
      ElMessage.success('获取列表数据成功');
    } else {
      ElMessage.error('获取列表数据失败');
    }
  } catch (error) {
    console.error('获取列表数据失败:', error);
    ElMessage.error('获取列表数据失败');
  } finally {
    loading.value = false;
  }
};

// 打开创建对话框
const openCreateDialog = () => {
  dialogType.value = 'create';
  Object.assign(currentCategory, {
    id: undefined,
    name: '',
    parent: null,
    weight: 0,
    sort_order: 0
  });
  dialogVisible.value = true;
};

// 打开编辑对话框
const openEditDialog = (category: Category) => {
  dialogType.value = 'edit';
  Object.assign(currentCategory, { ...category });
  dialogVisible.value = true;
};

// 保存分类
const saveCategory = async () => {
  try {
    // 准备发送的数据，确保parent字段正确处理
    // const sendData = {
    //   ...currentCategory,
    //   parent: currentCategory.parent === 0 ? null : currentCategory.parent
    // };
    
    if (dialogType.value === 'create') {
      console.log('创建分类:', currentCategory);
      await createCategory(currentCategory);
      ElMessage.success('创建成功');
    } else {
    
      console.log('更新父级id:', currentCategory.parent);
      await updateCategory(currentCategory.id!, currentCategory);
      ElMessage.success('更新成功');
    }
    dialogVisible.value = false;
    fetchListData(); // 刷新列表
  } catch (error) {
    console.error('保存分类失败:', error);
    ElMessage.error('保存失败');
  }
};

// 删除分类
const handleDelete = async (id: number) => {
  try {
    await deleteCategory(id);
    ElMessage.success('删除成功');
    fetchListData(); // 刷新列表
  } catch (error) {
    console.error('删除分类失败:', error);
    ElMessage.error('删除失败');
  }
};

// 页面加载时调用API
onMounted(() => {
  fetchListData();
});
</script>

<template>
  <div class="test-container">
    <h1>分类管理</h1>
    
    <!-- 操作按钮 -->
    <div style="margin-bottom: 20px;">
      <el-button type="primary" @click="openCreateDialog">新增分类</el-button>
    </div>
    
    <div class="list-data">
      <el-card v-loading="loading" :bordered="false">
        <template #header>
          <div class="card-header">
            <span>分类列表</span>
            <el-button type="primary" @click="fetchListData">刷新数据</el-button>
          </div>
        </template>
        
        <!-- 数据表格 -->
        <el-table :data="listData" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="parent" label="父级ID" width="80" />
          <el-table-column prop="weight" label="权重" width="80" />
          <el-table-column prop="sort_order" label="排序" width="80" />
          <el-table-column prop="created_at" label="创建时间" width="160" />
          <el-table-column prop="updated_at" label="更新时间" width="160" />
          
          <!-- 操作列 -->
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div v-if="listData.length === 0 && !loading" class="empty-message">
          暂无数据
        </div>
      </el-card>
    </div>
    
    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogType === 'create' ? '新增分类' : '编辑分类'" 
      v-model="dialogVisible" 
      width="500px"
    >
      <el-form :model="currentCategory" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="name" required>
          <el-input v-model="currentCategory.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="父级ID" prop="parent">
          <el-input-number v-model="currentCategory.parent" :min="0" placeholder="请输入父级ID" />
        </el-form-item>
        <el-form-item label="权重" prop="weight">
          <el-input-number v-model="currentCategory.weight" :min="0" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="currentCategory.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCategory">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.test-container {
  padding: 20px;
}

.list-data {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-message {
  color: #909399;
  text-align: center;
  padding: 20px 0;
}
</style>