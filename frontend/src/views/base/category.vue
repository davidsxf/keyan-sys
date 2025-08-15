<template>
  <div class="category-container">
    <div class="category-header">
      <h1>类别管理</h1>
      <el-button type="primary" @click="handleAddCategory">添加类别</el-button>
    </div>
    
    <div class="category-content">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>类别列表</span>
          </div>
        </template>
        
        <el-tree
          v-if="categories.length > 0"
          :data="categories"
          :props="treeProps"
          :expand-on-click-node="false"
          :default-expand-all="true"
          node-key="id"
          ref="categoryTree"
        >
          <template #default="{ node, data }">{{ data.name }}</template>
          <template #suffix="{ node, data }">
            <div class="tree-node-actions">
              <el-button
                type="primary"
                size="small"
                @click.stop="handleAddChildCategory(data.id, node)"
              >
                添加子类别
              </el-button>
              <el-button
                type="warning"
                size="small"
                @click.stop="handleEditCategory(data)"
              >
                编辑
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click.stop="handleDeleteCategory(data.id, node)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-tree>
        
        <div v-else class="empty-state">
          <el-empty description="暂无分类数据"></el-empty>
        </div>
      </el-card>
    </div>
  </div>

  <!-- 添加/编辑分类对话框 -->
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑分类' : '添加分类'"
    width="500px"
  >
    <el-form :model="categoryForm" ref="categoryFormRef" :rules="formRules">
      <el-form-item label="分类名称" prop="name">
        <el-input v-model="categoryForm.name" placeholder="请输入分类名称"></el-input>
      </el-form-item>
      
      <el-form-item label="父分类" prop="parent">
        <el-select v-model="categoryForm.parent" placeholder="请选择父分类">
          <el-option :value="null" label="无父分类"></el-option>
          <el-option
            v-for="item in flatCategories"
            :key="item.id"
            :label="getCategoryPath(item)"
            :value="item.id"
            :disabled="isEdit && item.id === categoryForm.id"
          ></el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="权重" prop="weight">
        <el-input-number
          v-model="categoryForm.weight"
          :min="0"
          placeholder="请输入权重"
        ></el-input-number>
      </el-form-item>
      
      <el-form-item label="排序" prop="sort_order">
        <el-input-number
          v-model="categoryForm.sort_order"
          :min="0"
          placeholder="请输入排序号"
        ></el-input-number>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { 
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory,
} from "@/api/category";
import type { Category, CategoryResponse } from "@/api/category";

// 分类树数据
const categories = ref<Category[]>([]);
// 扁平化的分类列表，用于选择父分类
const flatCategories = ref<Category[]>([]);
// 分类树配置
const treeProps = {
  children: "children",
  label: "name",
};
// 对话框状态
const dialogVisible = ref(false);
// 是否为编辑状态
const isEdit = ref(false);
// 表单数据
const categoryForm = reactive<Category>({
  name: "",
  parent: null,
  weight: 0,
  sort_order: 0,
});
// 表单规则
const formRules = {
  name: [
    { required: true, message: "请输入分类名称", trigger: "blur" },
    { min: 1, max: 50, message: "分类名称长度应在1-50个字符之间", trigger: "blur" },
  ],
  weight: [
    { required: true, message: "请输入权重", trigger: "blur" },
  ],
  sort_order: [
    { required: true, message: "请输入排序号", trigger: "blur" },
  ],
};
// 表单引用
const categoryFormRef = ref<InstanceType<typeof ElForm>>();
// 树引用
const categoryTree = ref<InstanceType<typeof ElTree>>();

// 获取分类数据
const fetchCategories = async () => {
  try {
    const response = await getCategories();
    if (response.success) {
      categories.value = response.data;
      // 生成扁平化分类列表
      flatCategories.value = flattenCategories(response.data);
    } else {
      ElMessage.error("获取分类数据失败");
    }
  } catch (error) {
    console.error("获取分类数据异常:", error);
    ElMessage.error("获取分类数据异常");
  }
};

// 扁平化分类树
const flattenCategories = (categories: Category[]): Category[] => {
  const result: Category[] = [];

  const traverse = (nodes: Category[]) => {
    nodes.forEach((node) => {
      result.push(node);
      if (node.children && node.children.length > 0) {
        traverse(node.children);
      }
    });
  };

  traverse(categories);
  return result;
};

// 获取分类路径（用于选择框显示）
const getCategoryPath = (category: Category): string => {
  const path: string[] = [];
  let current: Category | undefined = category;

  while (current) {
    path.unshift(current.name);
    // 查找父分类
    current = flatCategories.value.find(item => item.id === current.parent);
  }

  return path.join(" / ");
};

// 处理添加分类
const handleAddCategory = () => {
  isEdit.value = false;
  // 重置表单
  Object.assign(categoryForm, {
    name: "",
    parent: null,
    weight: 0,
    sort_order: 0,
  });
  dialogVisible.value = true;
};

// 处理添加子分类
const handleAddChildCategory = (parentId: number, node: any) => {
  isEdit.value = false;
  // 重置表单
  Object.assign(categoryForm, {
    name: "",
    parent: parentId,
    weight: 0,
    sort_order: 0,
  });
  dialogVisible.value = true;
  // 展开父节点
  node.expanded = true;
};

// 处理编辑分类
const handleEditCategory = (data: Category) => {
  isEdit.value = true;
  // 设置表单数据
  Object.assign(categoryForm, {
    ...data,
  });
  dialogVisible.value = true;
};

// 处理删除分类
const handleDeleteCategory = async (id: number, node: any) => {
  try {
    await ElMessageBox.confirm("确定要删除该分类吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    const response = await deleteCategory(id);
    if (response.success) {
      ElMessage.success("删除成功");
      // 重新获取分类数据
      await fetchCategories();
    } else {
      ElMessage.error("删除失败");
    }
  } catch (error) {
    if (error === "cancel") return;
    console.error("删除分类异常:", error);
    ElMessage.error("删除分类异常");
  }
};

// 处理表单提交
const handleSubmit = async () => {
  try {
    // 验证表单
    await categoryFormRef.value?.validate();

    let response;
    if (isEdit.value) {
      // 编辑分类
      response = await updateCategory(categoryForm.id!, categoryForm);
    } else {
      // 添加分类
      response = await createCategory(categoryForm);
    }

    if (response.success) {
      ElMessage.success(isEdit.value ? "编辑成功" : "添加成功");
      dialogVisible.value = false;
      // 重新获取分类数据
      await fetchCategories();
    } else {
      ElMessage.error(isEdit.value ? "编辑失败" : "添加失败");
    }
  } catch (error) {
    console.error(isEdit.value ? "编辑分类异常:" : "添加分类异常:", error);
  }
};

// 初始化加载分类数据
onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.category-container {
  padding: 20px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tree-node-actions {
  display: flex;
  gap: 5px;
  margin-left: 10px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}
</style>
