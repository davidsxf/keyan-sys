<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <h3 class="font-bold text-lg mb-6">项目信息</h3>
    
    <form @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label for="projectName" class="block text-sm font-medium text-gray-700 mb-1">项目名称 <span class="text-red-500">*</span></label>
          <input type="text" id="projectName" v-model="formData.name" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
          <label for="projectCode" class="block text-sm font-medium text-gray-700 mb-1">项目编号</label>
          <input type="text" id="projectCode" v-model="formData.code" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" readonly>
        </div>
        <div>
          <label for="leader" class="block text-sm font-medium text-gray-700 mb-1">项目负责人 <span class="text-red-500">*</span></label>
          <input type="text" id="leader" v-model="formData.leader" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
          <label for="department" class="block text-sm font-medium text-gray-700 mb-1">所属部门 <span class="text-red-500">*</span></label>
          <select id="department" v-model="formData.department" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <option value="">请选择部门</option>
            <option value="计算机学院">计算机学院</option>
            <option value="材料学院">材料学院</option>
            <option value="物理系">物理系</option>
            <option value="数学系">数学系</option>
            <option value="医学院">医学院</option>
          </select>
        </div>
        <div>
          <label for="startDate" class="block text-sm font-medium text-gray-700 mb-1">开始日期 <span class="text-red-500">*</span></label>
          <input type="date" id="startDate" v-model="formData.startDate" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
          <label for="endDate" class="block text-sm font-medium text-gray-700 mb-1">结束日期 <span class="text-red-500">*</span></label>
          <input type="date" id="endDate" v-model="formData.endDate" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
          <label for="funding" class="block text-sm font-medium text-gray-700 mb-1">经费(万元) <span class="text-red-500">*</span></label>
          <input type="number" id="funding" v-model.number="formData.funding" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
          <label for="source" class="block text-sm font-medium text-gray-700 mb-1">经费来源 <span class="text-red-500">*</span></label>
          <select id="source" v-model="formData.source" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <option value="">请选择来源</option>
            <option value="国家自然科学基金">国家自然科学基金</option>
            <option value="科技部重点研发计划">科技部重点研发计划</option>
            <option value="教育部项目">教育部项目</option>
            <option value="省级科研项目">省级科研项目</option>
            <option value="市级科研项目">市级科研项目</option>
            <option value="横向合作项目">横向合作项目</option>
          </select>
        </div>
      </div>
      
      <div class="mb-6">
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">项目简介</label>
        <textarea id="description" v-model="formData.description" rows="4" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"></textarea>
      </div>
      
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-1">项目成员</label>
        <div class="space-y-3">
          <div class="flex items-center" v-for="(member, index) in formData.members" :key="index">
            <input type="text" v-model="member.name" placeholder="成员姓名" class="flex-grow px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <input type="text" v-model="member.role" placeholder="角色" class="flex-grow px-4 py-2 border-t border-b border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <input type="text" v-model="member.department" placeholder="所属部门" class="flex-grow px-4 py-2 border-t border-b border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <button type="button" @click="removeMember(index)" class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-r-lg transition-colors">
              <i class="fa fa-minus"></i>
            </button>
          </div>
          <button type="button" @click="addMember" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
            <i class="fa fa-plus mr-2"></i>添加成员
          </button>
        </div>
      </div>
      
      <div class="flex justify-end space-x-3">
        <button type="button" class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
          取消
        </button>
        <button type="submit" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          保存
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface ProjectMember {
  name: string
  role: string
  department: string
}

interface ProjectFormData {
  name: string
  code: string
  leader: string
  department: string
  startDate: string
  endDate: string
  funding: number
  source: string
  description: string
  members: ProjectMember[]
}

const formData = ref<ProjectFormData>({
  name: '',
  code: '',
  leader: '',
  department: '',
  startDate: '',
  endDate: '',
  funding: 0,
  source: '',
  description: '',
  members: [
    { name: '', role: '', department: '' }
  ]
})

const generateProjectCode = () => {
  if (!formData.value.name || !formData.value.startDate) return
  
  const year = formData.value.startDate.split('-')[0]
  let category = 'GEN'
  
  if (formData.value.name.includes('人工智能') || formData.value.name.includes('机器学习')) {
    category = 'AI'
  } else if (formData.value.name.includes('材料') || formData.value.name.includes('化学')) {
    category = 'MAT'
  } else if (formData.value.name.includes('物理') || formData.value.name.includes('量子')) {
    category = 'PHY'
  } else if (formData.value.name.includes('医学') || formData.value.name.includes('生物')) {
    category = 'MED'
  } else if (formData.value.name.includes('数学') || formData.value.name.includes('统计')) {
    category = 'MATH'
  }
  
  // 随机生成3位数字
  const randomNum = Math.floor(100 + Math.random() * 900)
  
  formData.value.code = `${year}-${category}-${randomNum}`
}

const addMember = () => {
  formData.value.members.push({ name: '', role: '', department: '' })
}

const removeMember = (index: number) => {
  if (formData.value.members.length > 1) {
    formData.value.members.splice(index, 1)
  }
}

const handleSubmit = () => {
  // 这里可以添加表单验证和提交逻辑
  console.log('提交项目数据:', formData.value)
  // 模拟提交成功
  alert('项目保存成功！')
}

// 监听项目名称和开始日期变化，自动生成项目编号
watch([() => formData.value.name, () => formData.value.startDate], generateProjectCode)
</script>
    