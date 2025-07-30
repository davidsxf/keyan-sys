<template>
  <div class="p-6">
    <!-- 用户信息卡片 -->
    <el-card class="mb-6">
      <div class="flex items-center">
        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a6da627449jpeg.jpeg" class="mr-4" size="large"></el-avatar>
        <div class="flex-grow">
          <h2 class="text-xl font-bold">admin</h2>
          <p class="text-gray-500">超级管理员</p>
        </div>
        <div class="flex space-x-4">
          <div class="text-center">
            <p class="text-2xl font-bold">1234</p>
            <p class="text-sm text-gray-500">用户总量</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold">321</p>
            <p class="text-sm text-gray-500">系统消息</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold">5000</p>
            <p class="text-sm text-gray-500">数据量</p>
          </div>
        </div>
      </div>
    </el-card>

    <div class="mb-6">
      <h2 class="text-2xl font-bold mb-2">科研概览</h2>
      <p class="text-gray-600">欢迎使用科研管理系统，以下是您的科研数据概览</p>
    </div>
    
    <el-row :gutter="20" class="mb-6">
      <!-- 统计卡片 -->
      <el-col :span="6">
          <el-card class="stat-card" shadow="hover">
          <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">进行中项目</p>
            <h3 class="text-3xl font-bold">12</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
            <el-icon class="text-blue-600 text-xl"><FolderOpened /></el-icon>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <el-icon class="mr-1"><ArrowUp /></el-icon> 16%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card" shadow="hover">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">已发表论文</p>
            <h3 class="text-3xl font-bold">48</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
            <el-icon class="text-green-600 text-xl"><Document /></el-icon>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <el-icon class="mr-1"><ArrowUp /></el-icon> 8%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card" shadow="hover">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">专利申请</p>
            <h3 class="text-3xl font-bold">7</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
            <el-icon class="text-purple-600 text-xl"><Lightbulb /></el-icon>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-red-500 flex items-center">
            <el-icon class="mr-1"><ArrowDown /></el-icon> 3%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card" shadow="hover">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">经费余额</p>
            <h3 class="text-3xl font-bold">¥286,500</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
            <el-icon class="text-yellow-600 text-xl"><Money /></el-icon>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <el-icon class="mr-1"><ArrowUp /></el-icon> 22%
          </span>
          <span class="text-gray-500 ml-2">相比上季度</span>
        </div>
      </el-card>
    </el-col>
  </el-row>
    
    <el-row :gutter="20" class="mb-6">
      <!-- 图表区域 -->
      <el-col :span="16">
        <el-card>
          <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">项目进度</h3>
          <div class="text-sm text-gray-500">
            <el-select v-model="projectTimeRange" placeholder="选择时间范围" size="small">
              <el-option label="本季度" value="quarter"></el-option>
              <el-option label="本年度" value="year"></el-option>
              <el-option label="全部" value="all"></el-option>
            </el-select>
          </div>
        </div>
        <div class="h-80">
          <!-- 图表将在这里渲染 -->
          <canvas id="projectChart"></canvas>
        </div>
      </div>
      
      <el-col :span="8">
        <el-card>
          <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">论文发表</h3>
          <div class="text-sm text-gray-500">
            <el-select v-model="paperTimeRange" placeholder="选择时间范围" size="small">
              <el-option label="本年度" value="year"></el-option>
              <el-option label="近三年" value="threeYears"></el-option>
            </el-select>
          </div>
        </div>
        <div class="h-80">
          <!-- 图表将在这里渲染 -->
          <canvas id="paperChart"></canvas>
        </div>
      </el-card>
    </div>
  </el-row>
    
    <el-divider content-position="left">科研动态</el-divider>
    <el-row :gutter="20">
      <!-- 表格区域 -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">待办事项</h3>
          <el-button type="text" class="text-blue-600">查看全部</el-button>
        </div>
        <el-list class="w-full">
          <el-list-item class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
              <el-icon class="text-blue-600"><Calendar /></el-icon>
            </div>
            <div class="flex-grow">
              <p class="font-medium">项目进度报告提交</p>
              <p class="text-sm text-gray-500">截止日期: 2025-08-15</p>
            </div>
            <div class="flex-shrink-0">
              <el-tag type="warning" size="small">即将截止</el-tag>
            </div>
          </el-list-item>
          <el-list-item class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 flex items-center justify-center mr-3">
              <el-icon class="text-red-600"><FileText /></el-icon>
            </div>
            <div class="flex-grow">
              <p class="font-medium">论文修改意见回复</p>
              <p class="text-sm text-gray-500">截止日期: 2025-08-10</p>
            </div>
            <div class="flex-shrink-0">
              <el-tag type="danger" size="small">逾期</el-tag>
            </div>
          </el-list-item>
          <li class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center mr-3">
              <el-icon class="text-green-600"><Users /></el-icon>
            </div>
            <div class="flex-grow">
              <p class="font-medium">研究团队会议</p>
              <p class="text-sm text-gray-500">时间: 2025-08-05 14:00</p>
            </div>
            <div class="flex-shrink-0">
              <el-tag type="success" size="small">今天</el-tag>
            </div>
          </li>
        </el-list>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">最近发表</h3>
          <el-button type="text" class="text-blue-600">查看全部</el-button>
        </div>
        <el-list class="w-full">
          <el-list-item class="py-3">
            <p class="font-medium mb-1">基于深度学习的智能科研数据分析方法研究</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><el-icon class="mr-1"><User /></el-icon>张三, 李四, 王五</span>
              <span><el-icon class="mr-1"><JournalText /></el-icon>IEEE Transactions</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-07-15</span>
            </div>
          </li>
          <el-list-item class="py-3">
            <p class="font-medium mb-1">新型材料在能源存储中的应用研究</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><el-icon class="mr-1"><User /></el-icon>赵六, 钱七</span>
            <span><el-icon class="mr-1"><JournalText /></el-icon>Advanced Materials</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-06-28</span>
            </div>
          </li>
          <li class="py-3">
            <p class="font-medium mb-1">量子计算在密码学中的挑战与机遇</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><el-icon class="mr-1"><User /></el-icon>孙八, 周九, 吴十</span>
            <span><el-icon class="mr-1"><JournalText /></el-icon>Nature</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-06-10</span>
            </div>
          </li>
        </el-list>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Document, Lightbulb, Money, Calendar, FileText, Users, User, JournalText, ArrowUp, ArrowDown, Menu, Grid } from '@element-plus/icons-vue'
import { FolderOpened } from '@element-plus/icons-vue'
import Chart from 'chart.js/auto'


// 定义数据属性
const projectTimeRange = ref('quarter')
const paperTimeRange = ref('year')
const projectChart = ref<Chart | null>(null)
const paperChart = ref<Chart | null>(null)

onMounted(() => {
  // 初始化项目进度图表
  const projectCtx = document.getElementById('projectChart') as HTMLCanvasElement
  projectChart.value = new Chart(projectCtx, {
    type: 'bar',
    data: {
      labels: ['项目A', '项目B', '项目C', '项目D', '项目E', '项目F'],
      datasets: [{
        label: '完成度 (%)',
        data: [75, 45, 90, 60, 30, 80],
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(54, 162, 235, 0.7)'
        ],
        borderColor: [
          'rgb(54, 162, 235)',
          'rgb(54, 162, 235)',
          'rgb(54, 162, 235)',
          'rgb(54, 162, 235)',
          'rgb(54, 162, 235)',
          'rgb(54, 162, 235)'
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
  })

  // 初始化论文发表图表
  const paperCtx = document.getElementById('paperChart') as HTMLCanvasElement
  paperChart.value = new Chart(paperCtx, {
    type: 'line',
    data: {
      labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      datasets: [{
        label: 'SCI论文',
        data: [3, 2, 5, 4, 6, 4, 5, 0, 0, 0, 0, 0],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.3,
        fill: true
      }, {
        label: '核心期刊',
        data: [5, 3, 4, 6, 3, 5, 4, 0, 0, 0, 0, 0],
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.3,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
})
</script>
    