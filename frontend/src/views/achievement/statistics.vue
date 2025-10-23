<template>
  <div class="container mx-auto py-4">
    <div class="card">
      <div class="card-header flex justify-between items-center">
        <h2 class="text-xl font-bold">成果统计</h2>
      </div>
      
      <!-- 筛选条件 -->
      <div class="card-body bg-gray-50 p-4">
        <el-form ref="filterForm" :model="filterForm" layout="inline" size="small">
          <el-form-item label="统计维度">
            <el-radio-group v-model="filterForm.dimension" @change="handleDimensionChange">
              <el-radio-button label="team">按团队</el-radio-button>
              <el-radio-button label="department">按部门</el-radio-button>
              <el-radio-button label="person">按个人</el-radio-button>
              <el-radio-button label="year">按年份</el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item v-if="filterForm.dimension !== 'year'" label="年份">
            <el-select v-model="filterForm.year" placeholder="请选择年份" clearable>
              <el-option 
                v-for="year in availableYears" 
                :key="year" 
                :label="year + '年'" 
                :value="year" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item v-if="filterForm.dimension === 'team' || filterForm.dimension === 'department'" label="筛选">
            <el-select 
              v-model="filterForm[filterForm.dimension]" 
              :placeholder="filterForm.dimension === 'team' ? '请选择团队' : '请选择部门'" 
              clearable
            >
              <el-option 
                v-for="item in filterForm.dimension === 'team' ? teams : departments" 
                :key="item.value" 
                :label="item.label" 
                :value="item.value" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSearch">统计</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 统计结果 -->
      <div class="card-body">
        <div v-loading="loading" class="mb-6">
          <!-- 统计卡片 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <el-card class="text-center">
              <template #header>
                <div class="card-header-title">总成果数</div>
              </template>
              <div class="text-3xl font-bold text-primary">{{ totalCount }}</div>
            </el-card>
            <el-card class="text-center">
              <template #header>
                <div class="card-header-title">高影响因子论文</div>
              </template>
              <div class="text-3xl font-bold text-success">{{ highImpactCount }}</div>
              <div class="text-sm text-gray-500">（IF > 5）</div>
            </el-card>
            <el-card class="text-center">
              <template #header>
                <div class="card-header-title">Q1/Q2论文</div>
              </template>
              <div class="text-3xl font-bold text-warning">{{ highQuartileCount }}</div>
            </el-card>
          </div>

          <!-- 图表 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <el-card>
              <template #header>
                <div class="card-header-title">{{ chartTitle }}分布</div>
              </template>
              <div class="h-64">
                <canvas ref="chartRef"></canvas>
              </div>
            </el-card>
            <el-card>
              <template #header>
                <div class="card-header-title">{{ chartTitle }}JCR分区统计</div>
              </template>
              <div class="h-64">
                <canvas ref="quartileChartRef"></canvas>
              </div>
            </el-card>
          </div>
        </div>

        <!-- 统计表格 -->
        <div v-if="!loading && statisticsData.length > 0">
          <el-table :data="statisticsData" style="width: 100%">
            <el-table-column 
              prop="name" 
              :label="filterForm.dimension === 'year' ? '年份' : filterForm.dimension === 'team' ? '团队' : filterForm.dimension === 'department' ? '部门' : '作者'" 
              width="180" 
            />
            <el-table-column prop="count" label="成果数量" width="120" />
            <el-table-column prop="highImpactCount" label="高影响因子论文" width="150">
              <template #default="scope">
                <div>
                  <span>{{ scope.row.highImpactCount }}</span>
                  <span v-if="scope.row.count > 0" class="text-sm text-gray-500 ml-2">
                    ({{ ((scope.row.highImpactCount / scope.row.count) * 100).toFixed(1) }}%)
                  </span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="avgImpactFactor" label="平均影响因子" width="150">
              <template #default="scope">
                {{ scope.row.avgImpactFactor ? scope.row.avgImpactFactor.toFixed(2) : '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="q1Count" label="Q1" width="80" />
            <el-table-column prop="q2Count" label="Q2" width="80" />
            <el-table-column prop="q3Count" label="Q3" width="80" />
            <el-table-column prop="q4Count" label="Q4" width="80" />
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="viewDetails(scope.row)">
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <div v-else-if="!loading" class="text-center py-12 text-gray-500">
          暂无统计数据
        </div>
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="detailDialogTitle" width="800px">
      <el-table v-loading="detailLoading" :data="detailData" style="width: 100%">
        <el-table-column prop="title" label="论文标题" show-overflow-tooltip />
        <el-table-column prop="journalName" label="期刊名称" width="180" show-overflow-tooltip />
        <el-table-column prop="publicationYear" label="发表年份" width="120" />
        <el-table-column prop="authors" label="作者" width="200" show-overflow-tooltip>
          <template #default="scope">
            {{ scope.row.authors.join(', ') }}
          </template>
        </el-table-column>
        <el-table-column prop="jcrQuartile" label="JCR分区" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.jcrQuartile" :type="getQuartileType(scope.row.jcrQuartile)">
              {{ scope.row.jcrQuartile }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="impactFactor" label="影响因子" width="120">
          <template #default="scope">
            {{ scope.row.impactFactor || '-' }}
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="!detailLoading && detailData.length > 0" class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="detailPagination.currentPage"
          v-model:page-size="detailPagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="detailTotal"
          @size-change="handleDetailSizeChange"
          @current-change="handleDetailCurrentChange"
        />
      </div>
      
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { achievementApi } from '@/api/achievement';
import { Chart, registerables } from 'chart.js';

// 注册Chart.js组件
Chart.register(...registerables);

// 筛选表单数据
const filterForm = reactive({
  dimension: 'team', // team, department, person, year
  year: undefined,
  team: undefined,
  department: undefined,
  person: undefined
});

// 可用年份选项
const availableYears = ref<number[]>([]);

// 团队和部门选项
const teams = ref<Array<{label: string; value: string}>>([]);
const departments = ref<Array<{label: string; value: string}>>([]);

// 统计数据
const statisticsData = ref<any[]>([]);
const loading = ref(false);
const totalCount = ref(0);
const highImpactCount = ref(0);
const highQuartileCount = ref(0);

// 图表引用
const chartRef = ref<HTMLCanvasElement>();
const quartileChartRef = ref<HTMLCanvasElement>();
let mainChart: Chart | null = null;
let quartileChart: Chart | null = null;

// 详情对话框
const detailDialogVisible = ref(false);
const detailDialogTitle = ref('');
const detailData = ref<any[]>([]);
const detailLoading = ref(false);
const detailTotal = ref(0);
const detailPagination = reactive({
  currentPage: 1,
  pageSize: 10
});
const currentDetailParams = ref<any>(null);

// 计算图表标题
const chartTitle = computed(() => {
  switch (filterForm.dimension) {
    case 'team':
      return filterForm.team ? `${teams.value.find(t => t.value === filterForm.team)?.label}` : '团队';
    case 'department':
      return filterForm.department ? `${departments.value.find(d => d.value === filterForm.department)?.label}` : '部门';
    case 'person':
      return '个人';
    case 'year':
      return '年份';
    default:
      return '';
  }
});

/**
 * 初始化可用年份
 */
const initAvailableYears = () => {
  const currentYear = new Date().getFullYear();
  const years: number[] = [];
  for (let year = currentYear; year >= 2010; year--) {
    years.push(year);
  }
  availableYears.value = years;
  // 默认选择当前年份
  filterForm.year = currentYear;
};

/**
 * 初始化团队和部门数据
 */
const initTeamsAndDepartments = () => {
  // 模拟数据，实际项目中应从API获取
  teams.value = [
    { label: 'AI研究团队', value: 'ai_team' },
    { label: '大数据团队', value: 'big_data_team' },
    { label: '云计算团队', value: 'cloud_team' },
    { label: '物联网团队', value: 'iot_team' },
    { label: '安全研究团队', value: 'security_team' }
  ];
  
  departments.value = [
    { label: '计算机科学部', value: 'cs_department' },
    { label: '电子工程部', value: 'ee_department' },
    { label: '自动化部', value: 'auto_department' },
    { label: '信息管理部', value: 'im_department' },
    { label: '网络工程部', value: 'ne_department' }
  ];
};

/**
 * 处理维度切换
 */
const handleDimensionChange = () => {
  // 清除其他筛选条件
  if (filterForm.dimension !== 'team') filterForm.team = undefined;
  if (filterForm.dimension !== 'department') filterForm.department = undefined;
  if (filterForm.dimension !== 'person') filterForm.person = undefined;
};

/**
 * 获取统计数据
 */
const fetchStatisticsData = async () => {
  loading.value = true;
  try {
    // 获取所有论文数据
    const papers = await achievementApi.getPapers();
    
    // 根据当前筛选条件处理数据
    let filteredPapers = papers;
    
    // 如果按年份筛选
    if (filterForm.dimension !== 'year' && filterForm.year) {
      filteredPapers = filteredPapers.filter(paper => paper.publication_year === filterForm.year);
    }
    
    // 生成统计数据
    const result = generateStatisticsData(filteredPapers);
    statisticsData.value = result.data;
    
    // 计算汇总数据
    totalCount.value = result.totalCount;
    highImpactCount.value = result.highImpactCount;
    highQuartileCount.value = result.highQuartileCount;
    
    // 更新图表
    await nextTick();
    updateCharts();
  } catch (error) {
    console.error('获取统计数据失败:', error);
    ElMessage.error('获取统计数据失败');
  } finally {
    loading.value = false;
  }
};

/**
 * 根据论文数据生成统计数据
 * @param papers 论文数据
 * @returns 统计结果
 */
const generateStatisticsData = (papers: any[]) => {
  let data: any[] = [];
  let totalCount = papers.length;
  let highImpactCount = 0;
  let highQuartileCount = 0;
  
  // 根据维度分组处理数据
  switch (filterForm.dimension) {
    case 'team':
      // 按团队统计（这里需要从作者关联的staff信息获取团队信息）
      // 由于API限制，暂时使用模拟团队数据
      data = teams.value
        .filter(team => !filterForm.team || team.value === filterForm.team)
        .map(team => {
          // 模拟按团队筛选论文
          const teamPapers = papers.filter(() => Math.random() > 0.3); // 模拟30%的概率不属于该团队
          return processGroupPapers(team.label, team.value, teamPapers);
        });
      break;
      
    case 'department':
      // 按部门统计（这里需要从作者关联的staff信息获取部门信息）
      // 由于API限制，暂时使用模拟部门数据
      data = departments.value
        .filter(dept => !filterForm.department || dept.value === filterForm.department)
        .map(dept => {
          // 模拟按部门筛选论文
          const deptPapers = papers.filter(() => Math.random() > 0.2); // 模拟20%的概率不属于该部门
          return processGroupPapers(dept.label, dept.value, deptPapers);
        });
      break;
      
    case 'person':
      // 按作者统计
      const authorMap = new Map<string, any[]>();
      
      // 按作者分组
      papers.forEach(paper => {
        // 获取所有作者（第一作者和通讯作者）
        const allAuthors = [...paper.first_authors, ...paper.corresponding_authors];
        
        allAuthors.forEach(author => {
          const authorId = author.id.toString();
          if (!authorMap.has(authorId)) {
            authorMap.set(authorId, []);
          }
          authorMap.get(authorId)!.push(paper);
        });
      });
      
      // 转换为数组并处理
      data = Array.from(authorMap.entries()).map(([authorId, authorPapers]) => {
        const firstPaper = authorPapers[0];
        const author = firstPaper.first_authors.find((a: any) => a.id.toString() === authorId) || 
                       firstPaper.corresponding_authors.find((a: any) => a.id.toString() === authorId);
        const authorName = author ? author.name : `作者${authorId}`;
        
        return processGroupPapers(authorName, authorId, authorPapers);
      });
      
      // 按成果数量排序
      data.sort((a, b) => b.count - a.count);
      break;
      
    case 'year':
      // 按年份统计
      const yearMap = new Map<number, any[]>();
      
      // 按年份分组
      papers.forEach(paper => {
        const year = paper.publication_year;
        if (!yearMap.has(year)) {
          yearMap.set(year, []);
        }
        yearMap.get(year)!.push(paper);
      });
      
      // 转换为数组并处理
      data = Array.from(yearMap.entries()).map(([year, yearPapers]) => {
        return processGroupPapers(`${year}年`, year, yearPapers);
      });
      
      // 按年份降序排序
      data.sort((a, b) => b.value - a.value);
      break;
  }
  
  // 计算总体高影响因子和高分区论文数量
  highImpactCount = data.reduce((sum, item) => sum + item.highImpactCount, 0);
  highQuartileCount = data.reduce((sum, item) => sum + (item.q1Count + item.q2Count), 0);
  
  return {
    data,
    totalCount,
    highImpactCount,
    highQuartileCount
  };
};

/**
 * 处理分组的论文数据
 * @param name 分组名称
 * @param value 分组值
 * @param papers 该分组的论文
 * @returns 统计结果
 */
const processGroupPapers = (name: string, value: any, papers: any[]) => {
  const count = papers.length;
  let q1Count = 0;
  let q2Count = 0;
  let q3Count = 0;
  let q4Count = 0;
  let highImpactCount = 0;
  let totalImpactFactor = 0;
  let impactFactorCount = 0;
  
  papers.forEach(paper => {
    // 统计JCR分区
    let jcrQuartile = paper.journal?.jcr_quartile;
    
    // 如果论文没有直接的分区信息，尝试从期刊指标中获取
    if (!jcrQuartile && paper.journal?.metrics) {
      // 查找对应年份的指标
      const metric = paper.journal.metrics.find((m: any) => m.year === paper.publication_year);
      if (metric) {
        jcrQuartile = metric.jcr_quartile;
      }
    }
    
    // 根据分区计数
    switch (jcrQuartile) {
      case 'Q1':
        q1Count++;
        break;
      case 'Q2':
        q2Count++;
        break;
      case 'Q3':
        q3Count++;
        break;
      case 'Q4':
        q4Count++;
        break;
    }
    
    // 统计影响因子
    let impactFactor = paper.journal?.impact_factor;
    
    // 如果论文没有直接的影响因子信息，尝试从期刊指标中获取
    if (!impactFactor && paper.journal?.metrics) {
      // 查找对应年份的指标
      const metric = paper.journal.metrics.find((m: any) => m.year === paper.publication_year);
      if (metric) {
        impactFactor = metric.impact_factor;
      }
    }
    
    // 统计高影响因子论文（IF > 5）
    if (impactFactor && impactFactor > 5) {
      highImpactCount++;
    }
    
    // 累计影响因子用于计算平均值
    if (impactFactor) {
      totalImpactFactor += impactFactor;
      impactFactorCount++;
    }
  });
  
  // 计算平均影响因子
  const avgImpactFactor = impactFactorCount > 0 ? totalImpactFactor / impactFactorCount : 0;
  
  return {
    name,
    value,
    count,
    q1Count,
    q2Count,
    q3Count,
    q4Count,
    highImpactCount,
    avgImpactFactor
  };
};

/**
 * 更新图表
 */
const updateCharts = () => {
  // 销毁现有图表
  if (mainChart) {
    mainChart.destroy();
  }
  if (quartileChart) {
    quartileChart.destroy();
  }
  
  if (statisticsData.value.length === 0) return;
  
  // 创建主要统计图表
  if (chartRef.value) {
    const ctx = chartRef.value.getContext('2d');
    if (ctx) {
      mainChart = new Chart(ctx, {
        type: filterForm.dimension === 'year' ? 'line' : 'bar',
        data: {
          labels: statisticsData.value.map(item => item.name),
          datasets: [
            {
              label: '成果数量',
              data: statisticsData.value.map(item => item.count),
              backgroundColor: 'rgba(64, 158, 255, 0.6)',
              borderColor: 'rgba(64, 158, 255, 1)',
              borderWidth: 1
            },
            {
              label: '高影响因子论文',
              data: statisticsData.value.map(item => item.highImpactCount),
              backgroundColor: 'rgba(103, 194, 58, 0.6)',
              borderColor: 'rgba(103, 194, 58, 1)',
              borderWidth: 1
            }
          ]
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
      });
    }
  }
  
  // 创建JCR分区统计图表
  if (quartileChartRef.value) {
    const ctx = quartileChartRef.value.getContext('2d');
    if (ctx) {
      quartileChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: statisticsData.value.map(item => item.name),
          datasets: [
            {
              label: 'Q1',
              data: statisticsData.value.map(item => item.q1Count),
              backgroundColor: 'rgba(245, 34, 45, 0.6)',
              borderColor: 'rgba(245, 34, 45, 1)',
              borderWidth: 1
            },
            {
              label: 'Q2',
              data: statisticsData.value.map(item => item.q2Count),
              backgroundColor: 'rgba(250, 173, 20, 0.6)',
              borderColor: 'rgba(250, 173, 20, 1)',
              borderWidth: 1
            },
            {
              label: 'Q3',
              data: statisticsData.value.map(item => item.q3Count),
              backgroundColor: 'rgba(64, 158, 255, 0.6)',
              borderColor: 'rgba(64, 158, 255, 1)',
              borderWidth: 1
            },
            {
              label: 'Q4',
              data: statisticsData.value.map(item => item.q4Count),
              backgroundColor: 'rgba(144, 147, 153, 0.6)',
              borderColor: 'rgba(144, 147, 153, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            legend: {
              position: 'top'
            }
          }
        }
      });
    }
  }
};

/**
 * 查看详情
 * @param row 选中的统计行数据
 */
const viewDetails = async (row: any) => {
  currentDetailParams.value = {
    ...filterForm,
    targetValue: row.value,
    targetName: row.name
  };
  detailDialogTitle.value = `${row.name} - 成果详情`;
  detailPagination.currentPage = 1;
  await fetchDetailData();
  detailDialogVisible.value = true;
};

/**
 * 获取详情数据
 */
const fetchDetailData = async () => {
  if (!currentDetailParams.value) return;
  
  detailLoading.value = true;
  try {
    // 获取所有论文数据
    const papers = await achievementApi.getPapers();
    
    // 根据当前筛选条件过滤论文
    let filteredPapers = papers;
    
    // 按年份筛选
    if (currentDetailParams.value.dimension !== 'year' && currentDetailParams.value.year) {
      filteredPapers = filteredPapers.filter(paper => paper.publication_year === currentDetailParams.value.year);
    }
    
    // 根据维度进一步筛选
    switch (currentDetailParams.value.dimension) {
      case 'team':
      case 'department':
        // 由于API限制，暂时使用模拟筛选
        filteredPapers = filteredPapers.filter(() => Math.random() > 0.5);
        break;
      case 'person':
        // 按作者ID筛选
        filteredPapers = filteredPapers.filter(paper => {
          const allAuthors = [...paper.first_authors, ...paper.corresponding_authors];
          return allAuthors.some(author => author.id.toString() === currentDetailParams.value.targetValue.toString());
        });
        break;
      case 'year':
        // 按年份筛选
        filteredPapers = filteredPapers.filter(paper => paper.publication_year === currentDetailParams.value.targetValue);
        break;
    }
    
    // 转换数据格式
    const formattedData = filteredPapers.map(paper => {
      // 获取JCR分区
      let jcrQuartile = paper.journal?.jcr_quartile;
      if (!jcrQuartile && paper.journal?.metrics) {
        const metric = paper.journal.metrics.find((m: any) => m.year === paper.publication_year);
        if (metric) {
          jcrQuartile = metric.jcr_quartile;
        }
      }
      
      // 获取影响因子
      let impactFactor = paper.journal?.impact_factor;
      if (!impactFactor && paper.journal?.metrics) {
        const metric = paper.journal.metrics.find((m: any) => m.year === paper.publication_year);
        if (metric) {
          impactFactor = metric.impact_factor;
        }
      }
      
      return {
        id: paper.id,
        title: paper.title,
        journalName: paper.journal?.name || '-',
        publicationYear: paper.publication_year,
        authors: [...paper.first_authors, ...paper.corresponding_authors].map((a: any) => a.name),
        jcrQuartile,
        impactFactor
      };
    });
    
    // 排序
    formattedData.sort((a, b) => b.publicationYear - a.publicationYear);
    
    // 分页
    detailTotal.value = formattedData.length;
    const start = (detailPagination.currentPage - 1) * detailPagination.pageSize;
    const end = start + detailPagination.pageSize;
    detailData.value = formattedData.slice(start, end);
  } catch (error) {
    console.error('获取详情数据失败:', error);
    ElMessage.error('获取详情数据失败');
  } finally {
    detailLoading.value = false;
  }
};



/**
 * 获取JCR分区对应的标签类型
 * @param quartile JCR分区
 * @returns 标签类型
 */
const getQuartileType = (quartile: string) => {
  const typeMap: Record<string, string> = {
    'Q1': 'primary',
    'Q2': 'success',
    'Q3': 'warning',
    'Q4': 'info'
  };
  return typeMap[quartile] || 'default';
};

/**
 * 搜索
 */
const handleSearch = () => {
  fetchStatisticsData();
};

/**
 * 重置
 */
const handleReset = () => {
  filterForm.dimension = 'team';
  filterForm.year = new Date().getFullYear();
  filterForm.team = undefined;
  filterForm.department = undefined;
  filterForm.person = undefined;
  fetchStatisticsData();
};

/**
 * 处理详情分页大小变更
 * @param size 每页大小
 */
const handleDetailSizeChange = (size: number) => {
  detailPagination.pageSize = size;
  fetchDetailData();
};

/**
 * 处理详情当前页变更
 * @param current 当前页码
 */
const handleDetailCurrentChange = (current: number) => {
  detailPagination.currentPage = current;
  fetchDetailData();
};

// 监听详情对话框关闭
watch(detailDialogVisible, (newVal) => {
  if (!newVal) {
    detailData.value = [];
    currentDetailParams.value = null;
  }
});

// 组件挂载时初始化
onMounted(() => {
  initAvailableYears();
  initTeamsAndDepartments();
  fetchStatisticsData();
});
</script>

<style scoped>
.container {
  width: 100%;
  padding: 0 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.card-body {
  padding: 20px;
}

.card-header-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

/* 响应式布局调整 */
@media (max-width: 768px) {
  .grid-cols-1\/2 {
    grid-template-columns: 1fr;
  }
  
  .grid-cols-3 {
    grid-template-columns: 1fr;
  }
}
</style>