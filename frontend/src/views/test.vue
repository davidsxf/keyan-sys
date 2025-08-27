<!-- CategoryManagement.vue -->
<template>
  <div class="category-management">
    <el-button type="primary" @click="showCreateDialog">添加分类</el-button>
    
    <el-table :data="categories" row-key="id" default-expand-all>
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="weight" label="权重" width="100" />
      <el-table-column prop="sort_order" label="排序" width="100" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="editCategory(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteCategory(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="父分类">
          <el-select v-model="form.parent_id" clearable>
            <el-option
              v-for="cat in flatCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权重">
          <el-input-number v-model="form.weight" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Category, CategoryForm } from '@/api/category'
import { categoryApi } from '@/api/category'

const categories = ref<Category[]>([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number>()

const form = reactive<CategoryForm>({
  name: '',
  parent_id: null,
  weight: 0,
  sort_order: 0
})

// 计算扁平化的分类列表用于下拉选择
const flatCategories = computed(() => {
  const flatten = (items: Category[]): Category[] => {
    return items.reduce((acc: Category[], item) => {
      acc.push({ ...item, children: undefined })
      if (item.children) {
        acc.push(...flatten(item.children))
      }
      return acc
    }, [])
  }
  return flatten(categories.value)
})

const dialogTitle = computed(() => isEditing.value ? '编辑分类' : '添加分类')

const loadCategories = async () => {
  try {
    categories.value = await categoryApi.getCategories()
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const showCreateDialog = () => {
  isEditing.value = false
  editingId.value = undefined
  Object.assign(form, {
    name: '',
    parent_id: null,
    weight: 0,
    sort_order: 0
  })
  dialogVisible.value = true
}

const editCategory = (category: Category) => {
  isEditing.value = true
  editingId.value = category.id
  Object.assign(form, {
    name: category.name,
    parent_id: category.parent_id,
    weight: category.weight,
    sort_order: category.sort_order
  })
  dialogVisible.value = true
}

const submitForm = async () => {
  try {
    if (isEditing.value && editingId.value) {
      await categoryApi.updateCategory(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await categoryApi.createCategory(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadCategories()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteCategory = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该分类？', '警告', { type: 'warning' })
    await categoryApi.deleteCategory(id)
    ElMessage.success('删除成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadCategories()
})
</script>