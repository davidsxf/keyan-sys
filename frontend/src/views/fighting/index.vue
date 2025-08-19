<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { http } from '@/utils/http';

defineOptions({
  name: "Fighting"
});

// 定义响应式变量存储API数据
const apiData = ref<{ message?: string }>({});
const loading = ref(false);

// 调用后端测试API的函数
const fetchTestData = async () => {
  loading.value = true;
  try {
    const response = await http.get('/api/v1/test');
    apiData.value = response;
    console.log(response);

    ElMessage.success('获取数据成功');
  } catch (error) {
    // console.error('获取数据失败:', error);
    ElMessage.error('获取数据失败');
  } finally {
    loading.value = false;
  }
};

// 页面加载时调用API
onMounted(() => {
  fetchTestData();
});
</script>

<template>
  <div class="fighting-container">
    <h1>加油</h1>
    <div class="api-data">
      <el-card v-loading="loading" :bordered="false">
        <template #header>
          <div class="card-header">
            <span>后端测试API数据</span>
          </div>
        </template>
        <div v-if="apiData.message" class="success-message">
          {{ apiData.message }}
        </div>
        <div v-else-if="!loading" class="empty-message">
          暂无数据
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.fighting-container {
  padding: 20px;
}

.api-data {
  margin-top: 20px;
}

.success-message {
  color: #67c23a;
  font-size: 16px;
  text-align: center;
  padding: 20px 0;
}

.empty-message {
  color: #909399;
  text-align: center;
  padding: 20px 0;
}
</style>