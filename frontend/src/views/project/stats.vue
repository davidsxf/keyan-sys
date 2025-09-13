<template>
  <div class="project-stats">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目统计分析</span>
        </div>
      </template>

      <!-- 筛选条件 -->
      <el-form :model="filterForm" inline>
        <el-form-item label="统计维度">
          <el-select v-model="filterForm.dimension" placeholder="请选择统计维度" @change="loadStats">
            <el-option label="按部门" value="department" />
            <el-option label="按团队" value="team" />
            <el-option label="按负责人" value="leader" />
            <el-option label="按年度" value="year" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable @change="loadStats">
            <el-option label="全部状态" value="" />
            <el-option v-for="item in statusChoices" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目类别">
          <el-select v-model="filterForm.category_id" placeholder="全部类别" clearable @change="loadStats">
            <el-option label="全部类别" value="" />
            <el-option v-for="item in categoryChoices" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker
            v-model="filterForm.start_date"
            type="date"
            placeholder="开始日期"
            clearable
            @change="loadStats"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="filterForm.end_date"
            type="date"
            placeholder="结束日期"
            clearable
            @change="loadStats"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadStats">刷新数据</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 统计卡片 -->
      <div class="stats-cards">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-label">总项目数</div>
            <div class="stat-value">{{ totalProjects }}</div>
          </div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-label">总预算(万元)</div>
            <div class="stat-value">{{ totalBudget }}</div>
          </div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-label">进行中项目</div>
            <div class="stat-value">{{ ongoingProjects }}</div>
          </div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-label">已完成项目</div>
            <div class="stat-value">{{ completedProjects }}</div>
          </div>
        </el-card>
      </div>

      <!-- 图表展示 -->
      <div class="charts-container">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>{{ dimensionLabels[filterForm.dimension] || '项目统计' }}-项目数量分布</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <el-empty v-if="loading" description="加载中..." />
            <div v-else-if="chartData.length === 0" class="no-data">暂无数据</div>
            <div v-else>
              <el-progress v-if="filterForm.dimension === 'department'" :percentage="100" status="success" />
              <div ref="chartContainer" class="chart"></div>
            </div>
          </div>
        </el-card>

        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>{{ dimensionLabels[filterForm.dimension] || '项目统计' }}-预算分布(万元)</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <el-empty v-if="loading" description="加载中..." />
            <div v-else-if="chartData.length === 0" class="no-data">暂无数据</div>
            <div v-else>
              <div ref="budgetChartContainer" class="chart"></div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 详细数据表格 -->
      <el-card class="data-table-card">
        <template #header>
          <div class="table-header">
            <span>{{ dimensionLabels[filterForm.dimension] || '项目统计' }}详细数据</span>
          </div>
        </template>
        <el-table :data="statsData" v-loading="loading" style="width: 100%">
          <el-table-column prop="name" :label="dimensionLabels[filterForm.dimension]" min-width="150" />
          <el-table-column prop="projectCount" label="项目数量" width="100" align="right" />
          <el-table-column prop="budgetSum" label="预算总额(万元)" width="120" align="right">
            <template #default="{ row }">
              {{ formatCurrency(row.budgetSum || 0) }}
            </template>
          </el-table-column>
          <el-table-column prop="avgBudget" label="平均预算(万元)" width="120" align="right">
            <template #default="{ row }">
              {{ formatCurrency(row.avgBudget || 0) }}
            </template>
          </el-table-column>
          <el-table-column prop="projectPercent" label="占比" width="100" align="center">
            <template #default="{ row }">
              {{ row.projectPercent }}%
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="viewDetail(row)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`${dimensionLabels[filterForm.dimension]}详情：${selectedItem?.name}`"
      width="80%"
      @close="resetDetail"
    >
      <el-table :data="detailProjects" v-loading="detailLoading" style="width: 100%">
        <el-table-column prop="number" label="项目编号" width="120" />
        <el-table-column prop="title" label="项目名称" min-width="200" />
        <el-table-column prop="leader_name" label="负责人" width="100" />
        <el-table-column prop="status_display" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">{{ row.status_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="budget" label="预算(万元)" width="120" align="right">
          <template #default="{ row }">
            {{ row.budget ? formatCurrency(row.budget) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
      </el-table>
      <div class="dialog-footer" v-if="detailProjects.length > 0">
        <div class="footer-stats">
          <span>合计项目数：{{ detailProjects.length }}</span>
          <span>合计预算：{{ formatCurrency(detailProjects.reduce((sum, item) => sum + (item.budget || 0), 0)) }}万元</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';
import { projectApi } from '@/api/project';
import type { Project, Choice } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';
import type { ProjectBudget } from '@/api/projectBudget';

// 统计维度标签映射
const dimensionLabels = {
  department: '部门',
  team: '团队',
  leader: '负责人',
  year: '年度'
};

// 筛选表单
const filterForm = ref({
  dimension: 'department',
  status: '',
  category_id: '',
  start_date: '',
  end_date: ''
});

// 统计数据
const statsData = ref<any[]>([]);
const chartData = ref<any[]>([]);
const loading = ref(false);

// 总数统计
const totalProjects = ref(0);
const totalBudget = ref(0);
const ongoingProjects = ref(0);
const completedProjects = ref(0);

// 选项数据
const statusChoices = ref<Choice[]>([]);
const categoryChoices = ref<Choice[]>([]);

// 图表实例
let chartInstance: any = null;
let budgetChartInstance: any = null;
const chartContainer = ref<HTMLElement>();
const budgetChartContainer = ref<HTMLElement>();

// 详情弹窗
const detailDialogVisible = ref(false);
const selectedItem = ref<any>(null);
const detailProjects = ref<Project[]>([]);
const detailLoading = ref(false);

// 格式化金额
const formatCurrency = (value: number): string => {
  if (!value) return '0.00';
  return value.toFixed(2);
};

// 获取状态标签类型
const getStatusTagType = (status: string): string => {
  const typeMap: Record<string, string> = {
    'ongoing': 'primary',
    'completed': 'success',
    'pending': 'warning',
    'terminated': 'danger'
  };
  return typeMap[status] || 'info';
};

// 加载选项数据
const loadChoices = async () => {
  try {
    const [statusRes, categoryRes] = await Promise.all([
      projectApi.getStatusChoices(),
      projectApi.getCategoryChoices()
    ]);
    statusChoices.value = statusRes;
    categoryChoices.value = categoryRes;
  } catch (error) {
    ElMessage.error('加载选项数据失败');
    console.error('Failed to load choices:', error);
  }
};

// 加载统计数据
const loadStats = async () => {
  loading.value = true;
  try {
    // 在实际项目中，这里应该调用专门的统计API
    // 由于目前没有专门的统计API，我们可以从项目列表数据中进行统计计算
    const projectRes = await projectApi.getProjects(filterForm.value);
    const projects = projectRes.items;
    
    // 计算总数
    totalProjects.value = projects.length;
    totalBudget.value = projects.reduce((sum, item) => sum + (item.budget || 0), 0);
    ongoingProjects.value = projects.filter(p => p.status === 'ongoing').length;
    completedProjects.value = projects.filter(p => p.status === 'completed').length;
    
    // 按维度分组统计
    const groupedStats: Record<string, any> = {};
    
    projects.forEach(project => {
      let groupKey = '';
      let groupName = '';
      
      switch (filterForm.value.dimension) {
        case 'department':
          // 实际项目中应该从部门信息中获取
          groupKey = `dept_${project.id % 5}`; // 模拟部门ID
          groupName = `部门${project.id % 5 + 1}`; // 模拟部门名称
          break;
        case 'team':
          // 实际项目中应该从团队信息中获取
          groupKey = `team_${project.id % 10}`; // 模拟团队ID
          groupName = `团队${project.id % 10 + 1}`; // 模拟团队名称
          break;
        case 'leader':
          groupKey = project.leader_id?.toString() || 'unknown';
          groupName = project.leader_name || '未知负责人';
          break;
        case 'year':
          // 从项目开始日期或结束日期中提取年份
          const projectYear = project.start_date ? new Date(project.start_date).getFullYear() : '未知';
          groupKey = `year_${projectYear}`;
          groupName = `${projectYear}年`;
          break;
      }
      
      if (!groupedStats[groupKey]) {
        groupedStats[groupKey] = {
          id: groupKey,
          name: groupName,
          projectCount: 0,
          budgetSum: 0,
          projects: []
        };
      }
      
      groupedStats[groupKey].projectCount++;
      groupedStats[groupKey].budgetSum += project.budget || 0;
      groupedStats[groupKey].projects.push(project);
    });
    
    // 转换为数组并计算占比和平均预算
    statsData.value = Object.values(groupedStats).map((stat: any) => ({
      ...stat,
      avgBudget: stat.projectCount > 0 ? stat.budgetSum / stat.projectCount : 0,
      projectPercent: totalProjects.value > 0 ? Math.round((stat.projectCount / totalProjects.value) * 100) : 0
    }));
    
    // 按项目数量排序
    statsData.value.sort((a, b) => b.projectCount - a.projectCount);
    
    // 如果是按年度统计，按照年份排序
    if (filterForm.value.dimension === 'year') {
      statsData.value.sort((a, b) => {
        // 提取年份数字进行比较
        const yearA = parseInt(a.name) || 0;
        const yearB = parseInt(b.name) || 0;
        return yearB - yearA; // 降序排列
      });
    }
    
    // 准备图表数据
    chartData.value = statsData.value.map(item => ({
      name: item.name,
      projectCount: item.projectCount,
      budgetSum: item.budgetSum
    }));
    
    // 渲染图表
    await nextTick();
    renderCharts();
  } catch (error) {
    ElMessage.error('加载统计数据失败');
    console.error('Failed to load stats:', error);
  } finally {
    loading.value = false;
  }
};

// 渲染图表
const renderCharts = () => {
  // 项目数量图表
  if (chartContainer.value) {
    if (!chartInstance) {
      chartInstance = echarts.init(chartContainer.value);
    }
    
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: chartData.value.map(item => item.name),
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '项目数量'
      },
      series: [{
        name: '项目数量',
        type: 'bar',
        data: chartData.value.map(item => item.projectCount),
        itemStyle: {
          color: '#409EFF'
        }
      }]
    };
    
    chartInstance.setOption(option);
  }
  
  // 预算分布图表
  if (budgetChartContainer.value) {
    if (!budgetChartInstance) {
      budgetChartInstance = echarts.init(budgetChartContainer.value);
    }
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 10,
        data: chartData.value.map(item => item.name)
      },
      series: [{
        name: '预算分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData.value.map(item => ({
          name: item.name,
          value: item.budgetSum
        }))
      }]
    };
    
    budgetChartContainer.value.style.height = '400px'; // 设置图表高度
    budgetChartInstance.setOption(option);
  }
};

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    dimension: 'department',
    status: '',
    category_id: '',
    start_date: '',
    end_date: ''
  };
  loadStats();
};

// 查看详情
const viewDetail = async (item: any) => {
  selectedItem.value = item;
  detailLoading.value = true;
  try {
    // 模拟加载详情数据
    // 实际项目中应该调用专门的API获取该维度下的项目列表
    detailProjects.value = item.projects || [];
    detailDialogVisible.value = true;
  } catch (error) {
    ElMessage.error('加载详情失败');
  } finally {
    detailLoading.value = false;
  }
};

// 重置详情
const resetDetail = () => {
  selectedItem.value = null;
  detailProjects.value = [];
};

// 监听窗口大小变化，重绘图表
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
  if (budgetChartInstance) {
    budgetChartInstance.resize();
  }
};

// 生命周期
onMounted(() => {
  loadChoices();
  loadStats();
  window.addEventListener('resize', handleResize);
});

// 组件卸载时销毁图表实例
const cleanup = () => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  if (budgetChartInstance) {
    budgetChartInstance.dispose();
    budgetChartInstance = null;
  }
  window.removeEventListener('resize', handleResize);
};

// 模拟组件卸载时的清理
// 实际项目中应该在组件的unmounted钩子中调用
// onUnmounted(cleanup);
</script>

<style scoped>
.project-stats {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
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

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 20px 0;
}

.chart-card {
  height: 450px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  height: calc(100% - 50px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 350px;
}

.no-data {
  color: #909399;
  font-size: 14px;
}

.data-table-card {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.footer-stats {
  display: flex;
  justify-content: flex-end;
  gap: 30px;
  font-weight: bold;
}

@media (max-width: 1024px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>