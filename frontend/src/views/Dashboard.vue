<template>
  <div class="p-6">
    <div class="mb-6">
      <h2 class="text-2xl font-bold mb-2">科研概览</h2>
      <p class="text-gray-600">欢迎使用科研管理系统，以下是您的科研数据概览</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <!-- 统计卡片 -->
      <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition-transform">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">进行中项目</p>
            <h3 class="text-3xl font-bold">12</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
            <i class="fa fa-folder-open text-blue-600 text-xl"></i>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <i class="fa fa-arrow-up mr-1"></i> 16%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition-transform">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">已发表论文</p>
            <h3 class="text-3xl font-bold">48</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
            <i class="fa fa-file-text-o text-green-600 text-xl"></i>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <i class="fa fa-arrow-up mr-1"></i> 8%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition-transform">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">专利申请</p>
            <h3 class="text-3xl font-bold">7</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
            <i class="fa fa-lightbulb-o text-purple-600 text-xl"></i>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-red-500 flex items-center">
            <i class="fa fa-arrow-down mr-1"></i> 3%
          </span>
          <span class="text-gray-500 ml-2">相比上月</span>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition-transform">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">经费余额</p>
            <h3 class="text-3xl font-bold">¥286,500</h3>
          </div>
          <div class="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
            <i class="fa fa-money text-yellow-600 text-xl"></i>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-green-500 flex items-center">
            <i class="fa fa-arrow-up mr-1"></i> 22%
          </span>
          <span class="text-gray-500 ml-2">相比上季度</span>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 图表区域 -->
      <div class="bg-white rounded-xl shadow-md p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">项目进度</h3>
          <div class="text-sm text-gray-500">
            <select class="bg-gray-100 rounded-md p-1">
              <option>本季度</option>
              <option>本年度</option>
              <option>全部</option>
            </select>
          </div>
        </div>
        <div class="h-80">
          <!-- 图表将在这里渲染 -->
          <canvas id="projectChart"></canvas>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">论文发表</h3>
          <div class="text-sm text-gray-500">
            <select class="bg-gray-100 rounded-md p-1">
              <option>本年度</option>
              <option>近三年</option>
            </select>
          </div>
        </div>
        <div class="h-80">
          <!-- 图表将在这里渲染 -->
          <canvas id="paperChart"></canvas>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
      <!-- 表格区域 -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">待办事项</h3>
          <button class="text-blue-600 hover:text-blue-800">查看全部</button>
        </div>
        <ul class="divide-y divide-gray-100">
          <li class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
              <i class="fa fa-calendar text-blue-600"></i>
            </div>
            <div class="flex-grow">
              <p class="font-medium">项目进度报告提交</p>
              <p class="text-sm text-gray-500">截止日期: 2025-08-15</p>
            </div>
            <div class="flex-shrink-0">
              <span class="inline-block px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">
                即将截止
              </span>
            </div>
          </li>
          <li class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 flex items-center justify-center mr-3">
              <i class="fa fa-file-text-o text-red-600"></i>
            </div>
            <div class="flex-grow">
              <p class="font-medium">论文修改意见回复</p>
              <p class="text-sm text-gray-500">截止日期: 2025-08-10</p>
            </div>
            <div class="flex-shrink-0">
              <span class="inline-block px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                逾期
              </span>
            </div>
          </li>
          <li class="py-3 flex items-center">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center mr-3">
              <i class="fa fa-users text-green-600"></i>
            </div>
            <div class="flex-grow">
              <p class="font-medium">研究团队会议</p>
              <p class="text-sm text-gray-500">时间: 2025-08-05 14:00</p>
            </div>
            <div class="flex-shrink-0">
              <span class="inline-block px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                今天
              </span>
            </div>
          </li>
        </ul>
      </div>
      
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-lg">最近发表</h3>
          <button class="text-blue-600 hover:text-blue-800">查看全部</button>
        </div>
        <ul class="divide-y divide-gray-100">
          <li class="py-3">
            <p class="font-medium mb-1">基于深度学习的智能科研数据分析方法研究</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><i class="fa fa-user mr-1"></i>张三, 李四, 王五</span>
              <span><i class="fa fa-journal-whills mr-1"></i>IEEE Transactions</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-07-15</span>
            </div>
          </li>
          <li class="py-3">
            <p class="font-medium mb-1">新型材料在能源存储中的应用研究</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><i class="fa fa-user mr-1"></i>赵六, 钱七</span>
              <span><i class="fa fa-journal-whills mr-1"></i>Advanced Materials</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-06-28</span>
            </div>
          </li>
          <li class="py-3">
            <p class="font-medium mb-1">量子计算在密码学中的挑战与机遇</p>
            <div class="flex items-center text-sm text-gray-500 mb-1">
              <span class="mr-3"><i class="fa fa-user mr-1"></i>孙八, 周九, 吴十</span>
              <span><i class="fa fa-journal-whills mr-1"></i>Nature</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-600">SCI一区</span>
              <span>2025-06-10</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

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
    