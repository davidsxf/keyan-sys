<template>
  <div class="staff-details">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>个人信息与统计</h2>
          <el-button type="primary" @click="goBack">
            返回员工列表
          </el-button>
        </div>
      </template>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>

      <!-- 员工基本信息 -->
      <div v-else class="staff-info-section">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ staffInfo.name }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ staffInfo.department_name }}</el-descriptions-item>
          <el-descriptions-item label="团队">{{ staffInfo.team_name }}</el-descriptions-item>
          <el-descriptions-item label="职位">{{ staffInfo.position }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ staffInfo.gender }}</el-descriptions-item>
          <el-descriptions-item label="生日">{{ formatDate(staffInfo.birthday) }}</el-descriptions-item>
          <el-descriptions-item label="入职日期">{{ formatDate(staffInfo.entry_date) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ staffInfo.status }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ staffInfo.email }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ staffInfo.phone }}</el-descriptions-item>
          <el-descriptions-item label="团队领导" span="2">
            <el-tag v-if="staffInfo.is_team_leader" type="success">是</el-tag>
            <span v-else>否</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 统计概览卡片 -->
      <div class="stats-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover" class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ achievementStats.firstAuthorCount }}</div>
                <div class="stat-label">第一作者成果</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ achievementStats.otherAuthorCount }}</div>
                <div class="stat-label">其他作者成果</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ projectStats.ledProjectsCount }}</div>
                <div class="stat-label">主持项目</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ projectStats.participatedProjectsCount }}</div>
                <div class="stat-label">参与项目</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 成果统计详情 -->
      <div class="section">
        <h3 class="section-title">成果统计</h3>
        <el-tabs v-model="achievementActiveTab">
          <el-tab-pane label="第一作者" name="firstAuthor">
            <el-table :data="firstAuthorAchievements" border>
              <el-table-column prop="title" label="成果标题" />
              <el-table-column prop="type" label="成果类型" />
              <el-table-column prop="published_date" label="发表日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.published_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="level" label="成果级别" />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="其他作者" name="otherAuthor">
            <el-table :data="otherAuthorAchievements" border>
              <el-table-column prop="title" label="成果标题" />
              <el-table-column prop="type" label="成果类型" />
              <el-table-column prop="published_date" label="发表日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.published_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="level" label="成果级别" />
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 项目统计详情 -->
      <div class="section">
        <h3 class="section-title">项目统计</h3>
        <el-tabs v-model="projectActiveTab">
          <el-tab-pane label="主持项目" name="ledProjects">
            <el-table :data="ledProjects" border>
              <el-table-column prop="title" label="项目名称" />
              <el-table-column prop="category_name" label="项目类别" />
              <el-table-column prop="start_date" label="开始日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.start_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="end_date" label="结束日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.end_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="budget" label="项目预算" width="120">
                <template #default="{ row }">
                  {{ formatCurrency(row.budget) }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="项目状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusTagType(row.status)">
                    {{ row.status_display || row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="参与项目" name="participatedProjects">
            <el-table :data="participatedProjects" border>
              <el-table-column prop="title" label="项目名称" />
              <el-table-column prop="category_name" label="项目类别" />
              <el-table-column prop="leader_name" label="项目负责人" />
              <el-table-column prop="start_date" label="开始日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.start_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="end_date" label="结束日期" width="120">
                <template #default="{ row }">
                  {{ formatDate(row.end_date) }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="项目状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusTagType(row.status)">
                    {{ row.status_display || row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { staffApi } from '@/api/staff'
import { achievementApi } from '@/api/achievement'
import { projectApi } from '@/api/project'
import type { Staff } from '@/api/staff'
import type { Achievement } from '@/api/achievement'
import type { Project } from '@/api/project'

// 路由
const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(true)
const staffInfo = reactive<Partial<Staff>>({
  name: '',
  department_name: '',
  team_name: '',
  position: '',
  gender: '',
  birthday: '',
  entry_date: '',
  status: '',
  email: '',
  phone: '',
  is_team_leader: false
})

// 成果统计数据
const achievementStats = reactive({
  firstAuthorCount: 0,
  otherAuthorCount: 0
})

const firstAuthorAchievements = ref<Achievement[]>([])
const otherAuthorAchievements = ref<Achievement[]>([])
const achievementActiveTab = ref('firstAuthor')

// 项目统计数据
const projectStats = reactive({
  ledProjectsCount: 0,
  participatedProjectsCount: 0
})

const ledProjects = ref<Project[]>([])
const participatedProjects = ref<Project[]>([])
const projectActiveTab = ref('ledProjects')

// 获取员工ID
const getStaffId = (): number | null => {
  const id = route.params.id
  // 添加ID参数的有效性检查
  if (id === undefined || id === null) {
    return null
  }
  
  const parsedId = typeof id === 'string' ? parseInt(id) : Number(id)
  // 确保ID是有效的数字且大于0
  return isNaN(parsedId) || parsedId <= 0 ? null : parsedId
}

// 加载员工信息
const loadStaffInfo = async () => {
  try {
    const staffId = getStaffId()
    // 检查ID是否有效
    if (!staffId) {
      return
    }
    const staff = await staffApi.getStaff(staffId)
    Object.assign(staffInfo, staff)
  } catch (error) {
    console.error('获取员工信息失败:', error)
    ElMessage.error('获取员工信息失败')
  }
}

// 加载成果统计
const loadAchievementStats = async () => {
  try {
    const staffId = getStaffId()
    // 检查ID是否有效
    if (!staffId) {
      return
    }
    
    // 获取论文列表（作为成果）
    const papers = await achievementApi.getPapers()
    // 根据员工ID和是否第一作者进行过滤
    const staffPapers = papers.filter(paper => 
      paper.first_authors.some(author => author.staff_id === staffId)
    )
    
    firstAuthorAchievements.value = staffPapers || []
    achievementStats.firstAuthorCount = staffPapers.length
    
    // 目前先使用相同的数据，后续可以根据实际API进行调整
    otherAuthorAchievements.value = []
    achievementStats.otherAuthorCount = 0
  } catch (error) {
    ElMessage.error('获取成果统计失败')
  }
}

// 加载项目统计
const loadProjectStats = async () => {
  try {
    const staffId = getStaffId()
    // 检查ID是否有效
    if (!staffId) {
      return
    }
    
    // 获取主持项目
    const ledProjectsResults = await projectApi.getProjects({
      leader_id: staffId
    })
    ledProjects.value = ledProjectsResults.items || []
    projectStats.ledProjectsCount = ledProjectsResults.total || ledProjects.value.length
    
    // 对于参与项目，由于API中没有直接提供participant_id参数，这里暂时使用相同数据
    // 后续需要根据后端实际提供的API进行调整
    participatedProjects.value = []
    projectStats.participatedProjectsCount = 0
  } catch (error) {
    console.error('获取项目统计失败:', error)
    ElMessage.error('获取项目统计失败')
  }
}

// 初始化加载数据
const initData = async () => {
  try {
    loading.value = true
    await Promise.all([
      loadStaffInfo(),
      loadAchievementStats(),
      loadProjectStats()
    ])
  } finally {
    loading.value = false
  }
}

// 返回员工列表
const goBack = () => {
  router.push('/base/staff')
}

// 格式化日期
const formatDate = (dateString?: string | null) => {
  // 添加更严格的类型和有效性检查
  if (!dateString || typeof dateString !== 'string' || dateString.trim() === '') {
    return ''
  }
  
  try {
    // 验证日期字符串格式，避免无效日期导致的问题
    const date = new Date(dateString)
    // 检查是否是有效日期
    if (isNaN(date.getTime())) {
      return ''
    }
    return date.toLocaleDateString()
  } catch (error) {
    // 捕获任何可能的日期处理错误
    return ''
  }
}

// 格式化货币
const formatCurrency = (value?: number) => {
  if (value === undefined || value === null) return '¥0'
  return `¥${value.toLocaleString()}`
}

// 获取状态标签类型
const getStatusTagType = (status?: string) => {
  if (!status) return ''
  
  const statusMap: Record<string, string> = {
    '进行中': 'primary',
    '已完成': 'success',
    '已暂停': 'warning',
    '已终止': 'danger'
  }
  
  return statusMap[status] || 'info'
}

// 生命周期
onMounted(() => {
  // 检查路由参数中是否有有效的ID
  const staffId = getStaffId()
  if (!staffId) {
    // 如果没有有效的ID，重定向到员工列表页面
    ElMessage.warning('缺少员工ID参数')
    router.push('/base/staff')
    return
  }
  
  // 只有在ID有效时才加载数据
  initData()
})
</script>

<style scoped>
.staff-details {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-container {
  padding: 20px 0;
}

.staff-info-section {
  margin-bottom: 30px;
}

.stats-overview {
  margin-bottom: 30px;
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  text-align: center;
  padding: 20px 0;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #1890ff;
}

.stat-label {
  font-size: 16px;
  color: #606266;
}

.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}
</style>