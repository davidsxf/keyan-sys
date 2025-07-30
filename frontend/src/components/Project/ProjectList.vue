<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-6">
      <div>
        <h3 class="font-bold text-lg">科研项目列表</h3>
        <p class="text-gray-500 text-sm">管理和跟踪所有科研项目</p>
      </div>
      <div class="mt-4 md:mt-0 flex space-x-2">
        <div class="relative">
          <input type="text" placeholder="搜索项目..." class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-full md:w-64">
          <i class="fa fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
        </div>
        <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors">
          <i class="fa fa-plus mr-2"></i>
          <span>新建项目</span>
        </button>
      </div>
    </div>
    
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">项目名称</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">负责人</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">起止日期</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">经费(万元)</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
            <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <i class="fa fa-folder-open text-blue-600"></i>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">人工智能在药物研发中的应用研究</div>
                  <div class="text-xs text-gray-500">2025-AI-001</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">李教授</div>
              <div class="text-xs text-gray-500">计算机学院</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              2025-01-15 至 2027-12-31
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              180.0
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                进行中
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <a href="#" class="text-indigo-600 hover:text-indigo-900 mr-3">查看</a>
              <a href="#" class="text-green-600 hover:text-green-900 mr-3">编辑</a>
              <a href="#" class="text-red-600 hover:text-red-900">删除</a>
            </td>
          </tr>
          <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                  <i class="fa fa-leaf text-green-600"></i>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">新型环保材料的制备与性能研究</div>
                  <div class="text-xs text-gray-500">2025-MAT-002</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">王教授</div>
              <div class="text-xs text-gray-500">材料学院</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              2025-03-01 至 2026-12-31
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              120.0
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                进行中
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <a href="#" class="text-indigo-600 hover:text-indigo-900 mr-3">查看</a>
              <a href="#" class="text-green-600 hover:text-green-900 mr-3">编辑</a>
              <a href="#" class="text-red-600 hover:text-red-900">删除</a>
            </td>
          </tr>
          <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-purple-100 rounded-full flex items-center justify-center">
                  <i class="fa fa-microchip text-purple-600"></i>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">量子计算与量子信息处理研究</div>
                  <div class="text-xs text-gray-500">2024-PHY-005</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">张教授</div>
              <div class="text-xs text-gray-500">物理系</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              2024-06-15 至 2027-06-14
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              350.0
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                进行中
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <a href="#" class="text-indigo-600 hover:text-indigo-900 mr-3">查看</a>
              <a href="#" class="text-green-600 hover:text-green-900 mr-3">编辑</a>
              <a href="#" class="text-red-600 hover:text-red-900">删除</a>
            </td>
          </tr>
          <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-red-100 rounded-full flex items-center justify-center">
                  <i class="fa fa-heartbeat text-red-600"></i>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">基于大数据的精准医疗研究</div>
                  <div class="text-xs text-gray-500">2023-MED-012</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">刘教授</div>
              <div class="text-xs text-gray-500">医学院</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              2023-09-01 至 2025-08-31
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              220.0
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                已完成
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <a href="#" class="text-indigo-600 hover:text-indigo-900 mr-3">查看</a>
              <a href="#" class="text-green-600 hover:text-green-900 mr-3">编辑</a>
              <a href="#" class="text-red-600 hover:text-red-900">删除</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="mt-6 flex items-center justify-between">
      <div class="text-sm text-gray-500">
        显示 1 至 4 条，共 24 条记录
      </div>
      <div class="flex space-x-2">
        <button class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white text-gray-500 hover:bg-gray-50 disabled:opacity-50" disabled>
          上一页
        </button>
        <button class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-blue-50 text-blue-600 hover:bg-blue-100">
          1
        </button>
        <button class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white text-gray-500 hover:bg-gray-50">
          2
        </button>
        <button class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white text-gray-500 hover:bg-gray-50">
          3
        </button>
        <button class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white text-gray-500 hover:bg-gray-50">
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Project {
  id: string
  name: string
  leader: string
  department: string
  startDate: string
  endDate: string
  funding: number
  status: string
}

const projects = ref<Project[]>([
  {
    id: '2025-AI-001',
    name: '人工智能在药物研发中的应用研究',
    leader: '李教授',
    department: '计算机学院',
    startDate: '2025-01-15',
    endDate: '2027-12-31',
    funding: 180.0,
    status: '进行中'
  },
  {
    id: '2025-MAT-002',
    name: '新型环保材料的制备与性能研究',
    leader: '王教授',
    department: '材料学院',
    startDate: '2025-03-01',
    endDate: '2026-12-31',
    funding: 120.0,
    status: '进行中'
  },
  {
    id: '2024-PHY-005',
    name: '量子计算与量子信息处理研究',
    leader: '张教授',
    department: '物理系',
    startDate: '2024-06-15',
    endDate: '2027-06-14',
    funding: 350.0,
    status: '进行中'
  },
  {
    id: '2023-MED-012',
    name: '基于大数据的精准医疗研究',
    leader: '刘教授',
    department: '医学院',
    startDate: '2023-09-01',
    endDate: '2025-08-31',
    funding: 220.0,
    status: '已完成'
  }
])
</script>
    