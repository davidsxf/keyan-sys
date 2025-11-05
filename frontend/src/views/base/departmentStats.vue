<template>
  <div class="department-stats">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>部门统计</h2>
          <el-button type="primary" @click="goBack">
            返回部门列表
          </el-button>
        </div>
      </template>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>

      <!-- 部门基本信息 -->
      <div v-else-if="departmentInfo.id" class="department-info-section">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="部门名称">{{ departmentInfo.name }}</el-descriptions-item>
          <el-descriptions-item label="所属父部门">{{ departmentInfo.parent_name || '无' }}</el-descriptions-item>
          <el-descriptions-item label="部门描述" span="2">{{ departmentInfo.description || '-' }}</el-descriptions-item>
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
                  <div class="stat-label">部门成员</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="stat-card">
                <div class="stat-content">
                  <div class="stat-number">{{ teamCount || 0 }}</div>
                  <div class="stat-label">下属团队</div>
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
                    {{ memberCount > 0 ? '未能获取该部门的成果数据' : '部门成员数据为空，无法统计成果' }}
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
                    {{ memberCount > 0 ? '未能获取该部门的项目数据' : '部门成员数据为空，无法统计项目' }}
                  </div>
                </template>
              </el-empty>
            </div>
          </template>
          <el-table v-else :data="ledProjects" border>
            <el-table-column prop="title" label="项目名称">
              <template #default="{ row }">
                <router-link :to="`/project/projectDetail?projectId=${row.id}`" class="project-link">
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
import { departmentApi } from '@/api/department'
import { achievementApi } from '@/api/achievement'
import { projectApi } from '@/api/project'
import { teamApi } from '@/api/team'
import type { Department } from '@/api/department'

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
  department_id?: number | string
  leader_id?: number
  author_id?: number
  type?: string
}

// 响应式数据
const loading = ref(true)
const departmentInfo = reactive<Partial<Department & { parent_name?: string }>>({
  id: 0,
  name: '',
  description: '',
  parent_name: ''
})

// 部门成员数量
const memberCount = ref(0)
// 部门成员列表
const departmentMembers = ref<number[]>([])
// 部门下属团队数量
const teamCount = ref(0)

// 成果统计数据
const leaderAchievements = ref<Paper[]>([])
const allAchievements = ref<Paper[]>([])
const achievementStats = reactive({
  leaderCount: 0,
  totalCount: 0
})

// 项目统计数据
const ledProjects = ref<Project[]>([])
const projectStats = reactive({
  ledProjectsCount: 0
})

/**
 * 获取部门ID
 * @returns 部门ID或null
 */
const getDepartmentId = (): number | null => {
  const id = route.params.id
  if (!id) return null
  
  const numId = Number(id)
  if (isNaN(numId) || numId <= 0) return null
  
  return numId
}

/**
 * 加载部门信息和成员列表
 */
const loadDepartmentInfo = async () => {
  try {
    const departmentId = getDepartmentId()
    if (!departmentId) {
      ElMessage.warning('部门ID无效')
      return
    }
    
    // 获取部门树
    const departments = await departmentApi.getDepartments()
    
    // 查找当前部门
    const findDepartment = (depts: Department[], id: number): Department | null => {
      for (const dept of depts) {
        if (dept.id === id) {
          return dept
        }
        if (dept.children && dept.children.length > 0) {
          const found = findDepartment(dept.children, id)
          if (found) return found
        }
      }
      return null
    }
    
    const currentDept = findDepartment(departments, departmentId)
    if (currentDept) {
      Object.assign(departmentInfo, currentDept)
      
      // 如果有父部门ID，查找父部门名称
      if (currentDept.parent_id) {
        const parentDept = findDepartment(departments, currentDept.parent_id)
        if (parentDept) {
          departmentInfo.parent_name = parentDept.name
        }
      }
      
      // 获取部门下的团队数量
      try {
        console.log('获取部门ID:', departmentId, '的团队数量');
        // 确保参数顺序正确，按照teamApi.getTeams的签名
        const teamsResponse = await teamApi.getTeams(undefined, departmentId);
        console.log('团队API响应:', teamsResponse);
        teamCount.value = teamsResponse.total;
        console.log('设置团队数量为:', teamCount.value);
      } catch (teamError) {
        console.error('获取团队数量失败:', teamError);
        // 作为备选，仍然使用子部门数量
        if (currentDept.children) {
          console.log('回退到子部门数量:', currentDept.children.length);
          teamCount.value = currentDept.children.length;
        }
      }
    }
    
    // 获取部门成员
    const apiUrl = `http://127.0.0.1:8000/api/v1/users/departments/${departmentId}/members/`
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`获取部门成员失败: ${response.status}`)
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
    departmentMembers.value = [...new Set(memberIds)]
    memberCount.value = departmentMembers.value.length
    
  } catch (error) {
    console.error('获取部门信息失败:', error)
    ElMessage.error('获取部门信息失败')
    departmentMembers.value = []
    memberCount.value = 0
  }
}

/**
 * 判断是否为第一作者/负责人（宽松匹配）
 * @param paper 论文对象
 * @returns 是否为第一作者/负责人
 */
const isFirstAuthor = (paper: any): boolean => {
  // 检查是否所有关键字段都是undefined
  const allFieldsUndefined = 
    paper.author_position === undefined && 
    paper.position === undefined &&
    paper.is_first_author === undefined &&
    paper.author_type === undefined &&
    paper.role === undefined &&
    paper.leader_id === undefined && 
    paper.principal_id === undefined && 
    paper.person_in_charge_id === undefined &&
    paper.order === undefined && 
    paper.rank === undefined && 
    paper.sort_order === undefined;
  
  // 如果所有关键字段都是undefined，采用宽松策略，默认视为第一作者
  // 这是为了确保在字段缺失的情况下能够正确统计成果
  if (allFieldsUndefined) {
    console.log(`论文ID: ${paper.id} - 所有作者位置字段均为undefined，采用宽松匹配，视为第一作者`);
    return true;
  }
  
  // 直接匹配明确的第一作者标识
  if (paper.author_position === 'first' || 
      paper.position === 'first' ||
      paper.is_first_author === true ||
      paper.author_type === 'first' ||
      paper.author_type === 'primary' ||
      paper.role === 'first' ||
      paper.role === 'leader') {
    console.log(`论文ID: ${paper.id} - 匹配到明确的第一作者标识`);
    return true
  }
  
  // 检查是否有负责人ID
  if (paper.leader_id || paper.principal_id || paper.person_in_charge_id) {
    console.log(`论文ID: ${paper.id} - 存在负责人ID`);
    return true
  }
  
  // 检查作者位置文本描述
  if (paper.author_position && typeof paper.author_position === 'string') {
    const positionLower = paper.author_position.toLowerCase()
    const isFirst = positionLower.includes('first') || 
           positionLower.includes('1st') || 
           positionLower.includes('第一') ||
           positionLower.includes('主要') ||
           positionLower.includes('主持') ||
           positionLower.includes('负责人');
    if (isFirst) {
      console.log(`论文ID: ${paper.id} - 从文本描述判断为第一作者`);
    }
    return isFirst;
  }
  
  // 检查排序（如果有order或rank字段）
  if (paper.order === 1 || paper.rank === 1 || paper.sort_order === 1) {
    console.log(`论文ID: ${paper.id} - 排序为第一`);
    return true
  }
  
  console.log(`论文ID: ${paper.id} - 未匹配第一作者条件`);
  return false
}

/**
 * 加载成果统计
 */
const loadAchievementStats = async () => {
  try {
    const departmentId = getDepartmentId()
    if (!departmentId) return
    
    console.log('开始获取部门成果数据，部门ID:', departmentId)
    
    // 重置成果数据
    leaderAchievements.value = []
    achievementStats.leaderCount = 0
    
    // 优先使用后端提供的getDepartmentPapers API获取部门成员作为第一作者的论文
    try {
      console.log('调用getDepartmentPapers API获取部门论文')
      const papers = await achievementApi.getDepartmentPapers(departmentId)
      
      // 处理返回的数据格式
      const paperList = Array.isArray(papers) ? papers : papers.data || papers.results || papers.items || []
      console.log('通过getDepartmentPapers API获取到的成果数:', paperList.length)
      
      // 由于API已经返回了部门成员作为第一作者的论文，直接使用
      leaderAchievements.value = paperList
      achievementStats.leaderCount = paperList.length
      
      console.log('成功使用后端API获取并设置部门成果数据')
      return
    } catch (apiError) {
      console.warn('调用getDepartmentPapers API失败，尝试备选方案:', apiError)
    }
    
    // 备选方案：使用支持department_id参数的通用API
    try {
      console.log('尝试使用带department_id参数的通用论文API')
      const papers = await achievementApi.getPapers({ department_id: departmentId })
      
      // 处理返回的数据格式
      const paperList = Array.isArray(papers) ? papers : papers.data || papers.results || papers.items || []
      console.log('通过通用API获取到的成果数:', paperList.length)
      
      // 过滤第一作者的论文
      const firstAuthorPapers = paperList.filter(paper => isFirstAuthor(paper))
      console.log('过滤后的第一作者论文数:', firstAuthorPapers.length)
      
      leaderAchievements.value = firstAuthorPapers
      achievementStats.leaderCount = firstAuthorPapers.length
      
      return
    } catch (genericApiError) {
      console.warn('使用通用API也失败，回退到手动匹配方案:', genericApiError)
    }
    
    // 最后的备选方案：只有在部门成员存在时才尝试手动匹配
    if (departmentMembers.value.length > 0) {
      console.log('尝试通过部门成员ID进行手动匹配，成员数量:', departmentMembers.value.length)
      
      // 获取所有论文
      const papers = await achievementApi.getPapers({})
      const paperList = Array.isArray(papers) ? papers : papers.data || papers.results || papers.items || []
      console.log('获取到的总论文数:', paperList.length)
      
      // 通过部门成员ID匹配成果
      const memberAchievements = paperList.filter(paper => {
        const authorId = paper.author_id || paper.leader_id || paper.principal_id
        const isMember = authorId && departmentMembers.value.includes(Number(authorId))
        if (isMember) {
          console.log(`论文ID: ${paper.id} 作者ID: ${authorId} 属于部门成员`)
        }
        return isMember
      })
      
      console.log('匹配到属于部门成员的论文数:', memberAchievements.length)
      
      // 过滤第一作者的论文
      const firstAuthorPapers = memberAchievements.filter(paper => isFirstAuthor(paper))
      console.log('最终筛选的第一作者论文数:', firstAuthorPapers.length)
      
      leaderAchievements.value = firstAuthorPapers
      achievementStats.leaderCount = firstAuthorPapers.length
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
    const departmentId = getDepartmentId()
    if (!departmentId) return
    
    // 获取项目数据
    const projects = await projectApi.getProjects({})
    const projectList = projects.data || projects.results || projects.items || []
    
    // 筛选属于当前部门的项目
    const departmentProjects = projectList.filter((project: any) => {
      return project.department_id === departmentId || 
             String(project.department_id) === String(departmentId) ||
             (project.department && project.department.id === departmentId)
    })
    
    // 如果通过department_id找不到，尝试通过负责人ID匹配
    if (departmentProjects.length === 0 && departmentMembers.value.length > 0) {
      console.log('尝试通过负责人ID匹配项目')
      const leaderMatchedProjects = projectList.filter((project: any) => {
        const leaderId = getProjectLeaderId(project)
        return leaderId !== null && departmentMembers.value.includes(leaderId)
      })
      
      console.log('通过负责人ID匹配到的项目数:', leaderMatchedProjects.length)
      
      if (leaderMatchedProjects.length > 0) {
        ledProjects.value = leaderMatchedProjects
        projectStats.ledProjectsCount = leaderMatchedProjects.length
        return
      }
    }
    
    ledProjects.value = departmentProjects
    projectStats.ledProjectsCount = departmentProjects.length
    
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
    
    // 加载部门信息和成员
    console.log('步骤1: 加载部门信息和成员')
    await loadDepartmentInfo()
    console.log('部门信息加载完成，成员数量:', departmentMembers.value.length)
    
    // 只有在成功获取部门成员后才尝试获取成果和项目
    if (departmentMembers.value.length > 0) {
      console.log('步骤2: 加载成果统计')
      await loadAchievementStats()
      console.log('成果统计加载完成，成果数量:', leaderAchievements.value.length)
      
      console.log('步骤3: 加载项目统计')
      await loadProjectStats()
      console.log('项目统计加载完成，项目数量:', ledProjects.value.length)
    } else {
      console.warn('未获取到部门成员数据，跳过成果和项目统计')
      ElMessage.warning('部门成员数据为空，无法进行成果和项目统计')
    }
    
    // 数据加载完成后的验证
    if (leaderAchievements.value.length === 0 && departmentMembers.value.length > 0) {
      console.log('部门成员存在但未找到匹配的成果，可能需要检查数据关联或调整筛选条件')
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
 * 返回部门列表
 */
const goBack = () => {
  router.push('/base/department')
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
  const departmentId = getDepartmentId()
  if (!departmentId) {
    ElMessage.warning('部门ID无效')
    router.push('/base/department')
    return
  }
  
  // 加载数据
  initData()
})
</script>

<style scoped>
.department-stats {
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

.department-info-section {
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