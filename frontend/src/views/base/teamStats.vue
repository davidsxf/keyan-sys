<template>
  <div class="team-stats">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>团队统计</h2>
          <el-button type="primary" @click="goBack">
            返回团队列表
          </el-button>
        </div>
      </template>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>

      <!-- 团队基本信息 -->
      <div v-else-if="teamInfo.id" class="team-info-section">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="团队名称">{{ teamInfo.name }}</el-descriptions-item>
          <el-descriptions-item label="所属部门">{{ teamInfo.department_name }}</el-descriptions-item>
          <el-descriptions-item label="研究领域" span="2">{{ teamInfo.research_field || '-' }}</el-descriptions-item>
          <el-descriptions-item label="团队描述" span="2">{{ teamInfo.description || '-' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 统计概览卡片 -->
        <div class="stats-overview">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ achievementStats.leaderCount || 0 }}</div>
                  <div class="stat-label">第一作者成果</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ projectStats.ledProjectsCount || 0 }}</div>
                  <div class="stat-label">主持项目</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ memberCount || 0 }}</div>
                  <div class="stat-label">团队成员</div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 成果统计详情 -->
        <div class="section">
          <h3 class="section-title">成果统计（第一作者）</h3>
          <template v-if="leaderAchievements.length === 0">
            <div class="empty-data">
              <el-empty description="暂无成果数据">
                <template #description>
                  <div class="empty-message">
                    {{ memberCount > 0 ? '未能获取该团队的成果数据' : '团队成员数据为空，无法统计成果' }}
                  </div>
                </template>
              </el-empty>
            </div>
          </template>
          <el-table v-else :data="leaderAchievements" border>
            <el-table-column prop="title" label="成果标题" />
            <el-table-column label="第一作者">
              <template #default="{ row }">
                {{ row.leader_name || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="published_date" label="发表日期" width="120">
              <template #default="{ row }">
                {{ formatDate(row.published_date) }}
              </template>
            </el-table-column>
            <el-table-column prop="level" label="成果级别" />
          </el-table>
        </div>

        <!-- 项目统计详情 -->
        <div class="section">
          <h3 class="section-title">项目统计（负责人）</h3>
          <template v-if="ledProjects.length === 0">
            <div class="empty-data">
              <el-empty description="暂无项目数据">
                <template #description>
                  <div class="empty-message">
                    {{ memberCount > 0 ? '未能获取该团队的项目数据' : '团队成员数据为空，无法统计项目' }}
                  </div>
                </template>
              </el-empty>
            </div>
          </template>
          <el-table v-else :data="ledProjects" border>
            <el-table-column prop="title" label="项目名称">
              <template #default="{ row }">
                <router-link :to="`/project/projectDetail?projectld=${row.id}`" class="project-link">
                  {{ row.title }}
                </router-link>
              </template>
            </el-table-column>
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
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { teamApi } from '@/api/team'
import { achievementApi } from '@/api/achievement'
import { projectApi } from '@/api/project'
import type { Team } from '@/api/team'

// 路由
const route = useRoute()
const router = useRouter()

// 定义接口类型
interface Project {
  id: number
  name: string
  status: string
  create_time: string
  budget: number
  leader_name: string
}

interface Paper {
  id: number
  title: string
  author_position: string
  publication_date: string
  journal: string
  author_names: string
  team_id?: number | string
  leader_id?: number
  author_id?: number
  type?: string
}

// 响应式数据
const loading = ref(true)
const teamInfo = reactive<Partial<Team>>({
  id: 0,
  name: '',
  description: '',
  research_field: '',
  department_name: ''
})

// 团队成员数量
const memberCount = ref(0)
// 团队成员列表
const teamMembers = ref<number[]>([])

// 成果统计数据
const leaderAchievements = ref<Paper[]>([])
const achievementStats = reactive({
  leaderCount: 0
})

// 项目统计数据
const ledProjects = ref<Project[]>([])
const projectStats = reactive({
  ledProjectsCount: 0
})

/**
 * 获取团队ID
 * @returns 团队ID或null
 */
const getTeamId = (): number | null => {
  const id = route.params.id
  if (!id) return null
  
  const numId = Number(id)
  if (isNaN(numId) || numId <= 0) return null
  
  return numId
}

/**
 * 加载团队信息和成员列表
 */
const loadTeamInfo = async () => {
  try {
    const teamId = getTeamId()
    if (!teamId) {
      ElMessage.warning('团队ID无效')
      return
    }
    
    // 1. 获取团队详情
    const teamData = await teamApi.getTeam(teamId)
    Object.assign(teamInfo, teamData)
    
    // 2. 使用指定的后端API地址获取团队成员
    const apiUrl = `http://127.0.0.1:8000/api/v1/users/teams/${teamId}/members/`
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`获取团队成员失败: ${response.status}`)
    }
    
    const data = await response.json()
    // 处理返回的数据格式
    const members = Array.isArray(data) ? data : data.data || data.results || data.members || []
    
    // 提取成员ID
    const memberIds = members
      .map((member: any) => {
        // 尝试不同的ID字段名
        return member.id || member.user_id || member.uid || member.user?.id
      })
      .filter((id: any) => id !== undefined && !isNaN(Number(id)))
      .map((id: any) => Number(id))
    
    // 去重
    teamMembers.value = [...new Set(memberIds)]
    memberCount.value = teamMembers.value.length
    
  } catch (error) {
    console.error('获取团队信息失败:', error)
    ElMessage.error('获取团队信息失败')
    teamMembers.value = []
    memberCount.value = 0
  }
}

/**
 * 判断是否为第一作者/负责人（宽松匹配）
 * @param paper 论文对象
 * @returns 是否为第一作者/负责人
 */
const isFirstAuthor = (paper: any): boolean => {
  // 直接匹配明确的第一作者标识
  if (paper.author_position === 'first' || 
      paper.position === 'first' ||
      paper.is_first_author === true ||
      paper.author_type === 'first' ||
      paper.author_type === 'primary' ||
      paper.role === 'first' ||
      paper.role === 'leader') {
    return true
  }
  
  // 检查是否有负责人ID
  if (paper.leader_id || paper.principal_id || paper.person_in_charge_id) {
    return true
  }
  
  // 检查作者位置文本描述
  if (paper.author_position && typeof paper.author_position === 'string') {
    const positionLower = paper.author_position.toLowerCase()
    return positionLower.includes('first') || 
           positionLower.includes('1st') || 
           positionLower.includes('第一') ||
           positionLower.includes('主要') ||
           positionLower.includes('主持') ||
           positionLower.includes('负责人')
  }
  
  // 检查排序（如果有order或rank字段）
  if (paper.order === 1 || paper.rank === 1 || paper.sort_order === 1) {
    return true
  }
  
  return false
}

/**
 * 加载成果统计
 */
const loadAchievementStats = async () => {
  try {
    const teamId = getTeamId()
    if (!teamId) return
    
    console.log('开始获取团队成果数据，团队ID:', teamId)
    
    // 使用专门的团队论文API获取数据
    try {
      // 调用新增的getTeamPapers方法，直接获取该团队成员作为第一作者的论文
      const papers = await achievementApi.getTeamPapers(teamId)
      
      // 处理返回的数据格式
      const paperList = Array.isArray(papers) ? papers : papers.data || papers.results || papers.items || []
      console.log('通过团队论文API获取到的成果数:', paperList.length)
      
      // 直接使用返回的论文列表
      leaderAchievements.value = paperList
      achievementStats.leaderCount = paperList.length
    } catch (teamApiError) {
      console.warn('团队论文API调用失败，尝试使用通用API:', teamApiError)
      
      // 备选方案：使用支持team_id参数的通用论文API
      const papers = await achievementApi.getPapers({ team_id: teamId })
      
      // 处理返回的数据格式
      const paperList = Array.isArray(papers) ? papers : papers.data || papers.results || papers.items || []
      console.log('通过通用API获取到的成果数:', paperList.length)
      
      leaderAchievements.value = paperList
      achievementStats.leaderCount = paperList.length
    }
    
    if (leaderAchievements.value.length === 0 && teamMembers.value.length > 0) {
      console.info('团队成员存在但未找到匹配的成果数据')
    }
    
  } catch (error) {
    console.error('获取成果统计失败:', error)
    ElMessage.error('获取成果统计出错')
    leaderAchievements.value = []
    achievementStats.leaderCount = 0
  }
}

/**
 * 获取项目负责人ID
 * @param project 项目对象
 * @returns 负责人ID或null
 */
const getProjectLeaderId = (project: any): number | null => {
  const leaderId = project.leader_id || project.principal_id || project.person_in_charge_id
  return leaderId ? Number(leaderId) : null
}

/**
 * 加载项目统计
 */
const loadProjectStats = async () => {
  try {
    const teamId = getTeamId()
    if (!teamId) return
    
    // 获取项目数据
    const projects = await projectApi.getProjects({})
    const projectList = projects.data || projects.results || projects.items || []
    
    // 筛选属于当前团队的项目
    const teamProjects = projectList.filter((project: any) => {
      return project.team_id === teamId || 
             String(project.team_id) === String(teamId) ||
             (project.team && project.team.id === teamId)
    })
    
    // 如果通过team_id找不到，尝试通过负责人ID匹配
    if (teamProjects.length === 0 && teamMembers.value.length > 0) {
      console.log('尝试通过负责人ID匹配项目')
      const leaderMatchedProjects = projectList.filter((project: any) => {
        const leaderId = getProjectLeaderId(project)
        return leaderId !== null && teamMembers.value.includes(leaderId)
      })
      
      console.log('通过负责人ID匹配到的项目数:', leaderMatchedProjects.length)
      
      if (leaderMatchedProjects.length > 0) {
        ledProjects.value = leaderMatchedProjects
        projectStats.ledProjectsCount = leaderMatchedProjects.length
        return
      }
    }
    
    ledProjects.value = teamProjects
    projectStats.ledProjectsCount = teamProjects.length
    
  } catch (error) {
    console.error('获取项目统计失败:', error)
    ElMessage.error('获取项目统计出错')
    ledProjects.value = []
    projectStats.ledProjectsCount = 0
  }
}

/**
 * 初始化加载数据
 */
const initData = async () => {
  try {
    loading.value = true
    
    console.log('开始初始化数据加载流程')
    
    // 加载团队信息和成员
    console.log('步骤1: 加载团队信息和成员')
    await loadTeamInfo()
    console.log('团队信息加载完成，成员数量:', teamMembers.value.length)
    
    // 只有在成功获取团队成员后才尝试获取成果和项目
    if (teamMembers.value.length > 0) {
      console.log('步骤2: 加载成果统计')
      await loadAchievementStats()
      console.log('成果统计加载完成，成果数量:', leaderAchievements.value.length)
      
      console.log('步骤3: 加载项目统计')
      await loadProjectStats()
      console.log('项目统计加载完成，项目数量:', ledProjects.value.length)
    } else {
      console.warn('未获取到团队成员数据，跳过成果和项目统计')
      ElMessage.warning('团队成员数据为空，无法进行成果和项目统计')
    }
    
    // 数据加载完成后的验证
    if (leaderAchievements.value.length === 0 && teamMembers.value.length > 0) {
      console.log('团队成员存在但未找到匹配的成果，可能需要检查数据关联或调整筛选条件')
    }
    
  } catch (error) {
    console.error('初始化数据加载失败:', error)
    ElMessage.error('加载数据时发生错误')
  } finally {
    loading.value = false
    console.log('数据加载流程结束')
  }
}

/**
 * 返回团队列表
 */
const goBack = () => {
  router.push('/base/team')
}

/**
 * 格式化日期
 * @param dateString 日期字符串
 * @returns 格式化后的日期字符串
 */
const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  try {
    return new Date(dateString).toLocaleDateString('zh-CN')
  } catch (error) {
    return '-'
  }
}

/**
 * 格式化货币
 * @param amount 金额
 * @returns 格式化后的货币字符串
 */
const formatCurrency = (amount?: number) => {
  if (amount === undefined || amount === null) return '-'
  return `¥${amount.toLocaleString('zh-CN')}`
}

/**
 * 获取状态标签类型
 * @param status 状态字符串
 * @returns Element Plus 标签类型
 */
const getStatusTagType = (status?: string) => {
  const statusMap: Record<string, string> = {
    'IN_PROGRESS': 'primary',
    'COMPLETED': 'success',
    'PENDING': 'warning',
    'CANCELLED': 'danger'
  }
  return statusMap[status || ''] || 'info'
}

// 生命周期
onMounted(() => {
  // 检查ID是否有效
  const teamId = getTeamId()
  if (!teamId) {
    ElMessage.warning('团队ID无效')
    router.push('/base/team')
    return
  }
  
  // 加载数据
  initData()
})
</script>

<style scoped>
.team-stats {
  padding: 20px;
}

.project-link {
  color: #1890ff;
  text-decoration: none;
}

.project-link:hover {
  color: #40a9ff;
  text-decoration: underline;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-container {
  padding: 20px 0;
}

.team-info-section {
  margin-bottom: 30px;
}

.stats-overview {
  margin: 30px 0;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  color: #666;
}

.section {
  margin: 30px 0;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-left: 10px;
  border-left: 4px solid #1890ff;
}

/* 空数据样式 */
.empty-data {
  padding: 40px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-message {
  margin-top: 10px;
  color: #909399;
  font-size: 14px;
  text-align: center;
}
</style>