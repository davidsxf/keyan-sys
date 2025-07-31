<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>科研管理系统</h1>
      <p>欢迎使用科研数据概览面板</p>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-content">
          <p class="stat-label">进行中项目</p>
          <p class="stat-value">12</p>
          <p class="stat-change">+16% 相比上月</p>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <p class="stat-label">已发表论文</p>
          <p class="stat-value">48</p>
          <p class="stat-change">+8% 相比上月</p>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <p class="stat-label">专利申请</p>
          <p class="stat-value">7</p>
          <p class="stat-change">-3% 相比上月</p>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <p class="stat-label">经费余额</p>
          <p class="stat-value">¥286,500</p>
          <p class="stat-change">+5% 相比上月</p>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-area">
      <el-card>
        <div class="card-header">
          <h2>项目进度图表</h2>
        </div>
        <div class="chart-container">
          <canvas id="projectChart"></canvas>
        </div>
      </el-card>
    </div>

    <!-- 最近活动区域 -->
    <div class="recent-activities">
      <el-card>
        <div class="card-header">
          <h2>最近活动</h2>
        </div>
        <el-list>
          <el-list-item v-for="activity in recentActivities" :key="activity.id">
            <span class="activity-time">{{ activity.time }}</span>
            <span class="activity-content">{{ activity.content }}</span>
          </el-list-item>
        </el-list>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';

// 注册Chart.js组件
Chart.register(...registerables);

// 图表引用
const projectChart = ref<Chart | null>(null);

// 最近活动数据
const recentActivities = ref([
  { id: 1, time: '今天 09:30', content: '项目A完成了75%的进度' },
  { id: 2, time: '昨天 14:15', content: '新提交了2篇论文' },
  { id: 3, time: '昨天 10:00', content: '申请了1项新专利' },
  { id: 4, time: '3天前', content: '获得了50万科研经费' },
]);

// 页面加载时初始化图表
onMounted(() => {
  const ctx = document.getElementById('projectChart') as HTMLCanvasElement;
  projectChart.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['项目A', '项目B', '项目C', '项目D'],
      datasets: [{
        label: '完成度 (%)',
        data: [75, 45, 90, 60],
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 99, 132, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(255, 206, 86, 0.7)'
        ],
        borderColor: [
          'rgb(54, 162, 235)',
          'rgb(255, 99, 132)',
          'rgb(75, 192, 192)',
          'rgb(255, 206, 86)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
});
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
}

.stats-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 200px;
}

.stat-content {
  padding: 20px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-change {
  font-size: 12px;
  color: #4caf50;
}

.charts-area {
  margin-bottom: 30px;
}

.chart-container {
  height: 300px;
}

.card-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.card-header h2 {
  font-size: 18px;
  font-weight: bold;
}

.recent-activities {
  margin-bottom: 30px;
}

.activity-time {
  color: #999;
  font-size: 12px;
  margin-right: 10px;
}

.activity-content {
  flex: 1;
}
</style>