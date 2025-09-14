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
          <el-select v-model="filterForm.dimension" placeholder="请选择统计维度" @change="loadStats" style="width: 100px">
            <el-option label="按部门" value="department" />
            <el-option label="按团队" value="team" />
            <el-option label="按负责人" value="leader" />
            <el-option label="按年度" value="year" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable @change="loadStats" style="width: 100px">
            <el-option label="全部状态" value="" />
            <el-option v-for="item in statusChoices" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目类别">
          <el-select v-model="filterForm.category_id" placeholder="全部类别" clearable @change="loadStats" style="width: 100px">
            <el-option label="全部类别" value="" />
            <el-option v-for="item in categoryChoices" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" style="width: 200px">
          <el-date-picker
            v-model="filterForm.start_date"
            type="date"
            placeholder="开始日期"
            clearable
            value-format="YYYY-MM-DD"
            @change="loadStats"
          />
        </el-form-item>
        <el-form-item label="结束日期" style="width: 200px">
          <el-date-picker
            v-model="filterForm.end_date"
            type="date"
            placeholder="结束日期"
            clearable
            value-format="YYYY-MM-DD"
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
            <div v-else class="chart-container">
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
            <div v-else class="chart-container">
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
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';
import { projectApi } from '@/api/project';
import type { Project, Choice } from '@/api/project';
import { projectBudgetApi } from '@/api/projectBudget';
import type { ProjectBudget } from '@/api/projectBudget';
import { departmentApi, teamApi, staffApi } from '@/api/staff';
import type { DepartmentOption, TeamOption, Staff } from '@/api/staff';


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

// 新增响应式变量
const departmentOptions = ref<DepartmentOption[]>([]);
const teamOptions = ref<TeamOption[]>([]);
const staffMap = ref<Map<number, Staff>>(new Map());

// 加载选项数据
const loadChoices = async () => {
  try {
    const [statusRes, categoryRes, deptRes, teamRes] = await Promise.all([
      projectApi.getStatusChoices(),
      projectApi.getCategoryChoices(),
      departmentApi.getDepartmentOptions(),
      teamApi.getTeamOptions()
    ]);
    statusChoices.value = statusRes;
    categoryChoices.value = categoryRes;
    departmentOptions.value = deptRes;
    teamOptions.value = teamRes;
  } catch (error) {
    ElMessage.error('加载选项数据失败');
    console.error('Failed to load choices:', error);
  }
};

// 渲染图表
const renderCharts = () => {
  console.log('开始渲染图表，当前维度:', filterForm.value.dimension);
  console.log('图表数据:', chartData.value);
  
  // 项目数量图表
  if (chartContainer.value) {
    try {
      // 1. 强制设置容器尺寸（关键修复）
      chartContainer.value.style.height = '400px';
      chartContainer.value.style.width = '100%';
      chartContainer.value.style.minHeight = '400px';
      chartContainer.value.style.minWidth = '100%';
      chartContainer.value.style.display = 'block';
      chartContainer.value.style.position = 'relative';
      chartContainer.value.style.visibility = 'visible';
      chartContainer.value.style.overflow = 'hidden';
      
      // 确保父容器也有正确的尺寸
      const parentElement = chartContainer.value.parentElement;
      if (parentElement) {
        parentElement.style.width = '100%';
        parentElement.style.height = '400px';
        parentElement.style.minHeight = '400px';
        parentElement.style.display = 'block';
        parentElement.style.position = 'relative';
      }
      
      // 确保祖父容器也有正确的尺寸
      const grandParentElement = parentElement?.parentElement;
      if (grandParentElement) {
        grandParentElement.style.width = '100%';
        grandParentElement.style.display = 'block';
      }
      
      // 2. 强制重排以确保尺寸生效
      chartContainer.value.offsetHeight; // 触发重排
      
      // 3. 检查容器是否有有效的尺寸
      const clientWidth = chartContainer.value.clientWidth;
      const clientHeight = chartContainer.value.clientHeight;
      
      console.log(`项目数量图表容器尺寸检查: ${clientWidth}x${clientHeight}`);
      
      if (clientWidth === 0 || clientHeight === 0) {
        console.warn(`项目数量图表容器尺寸无效 (${clientWidth}x${clientHeight})，计划重试...`);
        
        // 如果宽度为0，尝试直接设置一个固定宽度
        if (clientWidth === 0) {
          const cardElement = chartContainer.value.closest('.chart-card');
          if (cardElement) {
            const cardWidth = cardElement.clientWidth;
            console.log(`获取到卡片宽度: ${cardWidth}px`);
            chartContainer.value.style.width = `${cardWidth}px`;
          } else {
            // 如果无法获取卡片宽度，使用一个默认宽度
            chartContainer.value.style.width = '500px';
            console.log('使用默认宽度: 500px');
          }
        }
        
        // 重试一次
        setTimeout(() => renderCharts(), 300);
        return;
      }
      
      // 销毁旧实例（如果存在）
      if (chartInstance && !chartInstance.isDisposed()) {
        console.log('销毁旧的项目数量图表实例');
        chartInstance.dispose();
      }
      
      console.log(`正在使用有效尺寸初始化项目数量图表: ${clientWidth}x${clientHeight}`);
      // 使用强制尺寸的配置初始化
      chartInstance = echarts.init(chartContainer.value, null, {
        width: clientWidth,
        height: clientHeight
      });
      
      // 检查chartData是否有数据
      if (!chartData.value || chartData.value.length === 0) {
        console.warn('项目数量图表数据为空，使用默认数据');
        // 提供默认数据以便测试
        const defaultData = [
          { name: '测试部门1', projectCount: 5, budgetSum: 120 },
          { name: '测试部门2', projectCount: 3, budgetSum: 80 },
          { name: '测试部门3', projectCount: 7, budgetSum: 200 }
        ];
        
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
            data: defaultData.map(item => item.name),
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
            data: defaultData.map(item => item.projectCount),
            itemStyle: {
              color: '#409EFF'
            }
          }]
        };
        
        chartInstance.setOption(option);
      } else {
        // 使用实际数据
        console.log('使用实际数据渲染项目数量图表:', chartData.value);
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
    } catch (error) {
      console.error('渲染项目数量图表失败:', error);
      // 发生错误时重新初始化实例
      if (chartInstance) {
        chartInstance.dispose();
        chartInstance = null;
      }
      // 错误后重试
      setTimeout(() => renderCharts(), 300);
    }
  } else {
    console.error('项目数量图表容器未找到');
    // 添加重试机制
    setTimeout(() => {
      console.log('尝试重新获取图表容器...');
      renderCharts();
    }, 300);
  }
  
  // 预算分布图表
  if (budgetChartContainer.value) {
    try {
      // 1. 强制设置容器尺寸（关键修复）
      budgetChartContainer.value.style.height = '400px';
      budgetChartContainer.value.style.width = '100%';
      budgetChartContainer.value.style.minHeight = '400px';
      budgetChartContainer.value.style.minWidth = '100%';
      budgetChartContainer.value.style.display = 'block';
      budgetChartContainer.value.style.position = 'relative';
      budgetChartContainer.value.style.visibility = 'visible';
      budgetChartContainer.value.style.overflow = 'hidden';
      
      // 确保父容器也有正确的尺寸
      const parentElement = budgetChartContainer.value.parentElement;
      if (parentElement) {
        parentElement.style.width = '100%';
        parentElement.style.height = '400px';
        parentElement.style.minHeight = '400px';
        parentElement.style.display = 'block';
        parentElement.style.position = 'relative';
      }
      
      // 确保祖父容器也有正确的尺寸
      const grandParentElement = parentElement?.parentElement;
      if (grandParentElement) {
        grandParentElement.style.width = '100%';
        grandParentElement.style.display = 'block';
      }
      
      // 2. 强制重排以确保尺寸生效
      budgetChartContainer.value.offsetHeight; // 触发重排
      
      // 3. 检查容器是否有有效的尺寸
      const clientWidth = budgetChartContainer.value.clientWidth;
      const clientHeight = budgetChartContainer.value.clientHeight;
      
      console.log(`预算分布图表容器尺寸检查: ${clientWidth}x${clientHeight}`);
      
      if (clientWidth === 0 || clientHeight === 0) {
        console.warn(`预算分布图表容器尺寸无效 (${clientWidth}x${clientHeight})，计划重试...`);
        
        // 如果宽度为0，尝试直接设置一个固定宽度
        if (clientWidth === 0) {
          const cardElement = budgetChartContainer.value.closest('.chart-card');
          if (cardElement) {
            const cardWidth = cardElement.clientWidth;
            console.log(`获取到卡片宽度: ${cardWidth}px`);
            budgetChartContainer.value.style.width = `${cardWidth}px`;
          } else {
            // 如果无法获取卡片宽度，使用一个默认宽度
            budgetChartContainer.value.style.width = '500px';
            console.log('使用默认宽度: 500px');
          }
        }
        
        // 重试一次
        setTimeout(() => renderCharts(), 300);
        return;
      }
      
      // 销毁旧实例（如果存在）
      if (budgetChartInstance && !budgetChartInstance.isDisposed()) {
        console.log('销毁旧的预算分布图表实例');
        budgetChartInstance.dispose();
      }
      
      console.log(`正在使用有效尺寸初始化预算分布图表: ${clientWidth}x${clientHeight}`);
      // 使用强制尺寸的配置初始化
      budgetChartInstance = echarts.init(budgetChartContainer.value, null, {
        width: clientWidth,
        height: clientHeight
      });
      
      // 检查chartData是否有数据
      let budgetChartData;
      if (!chartData.value || chartData.value.length === 0) {
        console.warn('预算分布图表数据为空，使用默认数据');
        budgetChartData = [
          { name: '测试部门1', value: 120 },
          { name: '测试部门2', value: 80 },
          { name: '测试部门3', value: 200 }
        ];
      } else {
        budgetChartData = chartData.value.map(item => ({ name: item.name, value: item.budgetSum }));
      }
      
      const budgetOption = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c}万元 ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: budgetChartData.map(item => item.name)
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
          data: budgetChartData
        }]
      };
      
      console.log('渲染预算分布图表，数据:', budgetChartData);
      budgetChartInstance.setOption(budgetOption);
    } catch (error) {
      console.error('渲染预算分布图表失败:', error);
      // 发生错误时重新初始化实例
      if (budgetChartInstance) {
        budgetChartInstance.dispose();
        budgetChartInstance = null;
      }
      // 错误后重试
      setTimeout(() => renderCharts(), 300);
    }
  } else {
    console.error('预算分布图表容器未找到');
    // 添加重试机制
    setTimeout(() => {
      console.log('尝试重新获取预算分布图表容器...');
      renderCharts();
    }, 300);
  }
};

// 加载统计数据
const loadStats = async () => {
  loading.value = true;
  try {
    // 在实际项目中，这里应该调用专门的统计API
    // 由于目前没有专门的统计API，我们可以从项目列表数据中进行统计计算
    
    // 从filterForm中提取后端需要的参数，排除dimension
    const apiParams = {
      status: filterForm.value.status,
      category_id: filterForm.value.category_id,
      start_date: filterForm.value.start_date,
      end_date: filterForm.value.end_date
    };
    
    // 只传递非空参数
    const filteredParams = Object.fromEntries(
      Object.entries(apiParams).filter(([_, value]) => value !== '' && value !== undefined)
    );
    
    // 处理日期格式，确保后端能正确解析
    if (filteredParams.start_date) {
      // 将日期对象转换为ISO字符串格式，然后只取日期部分
      if (typeof filteredParams.start_date === 'object' && filteredParams.start_date instanceof Date) {
        filteredParams.start_date = filteredParams.start_date.toISOString().split('T')[0];
      } else if (typeof filteredParams.start_date === 'string') {
        // 如果已经是字符串，确保格式正确
        const date = new Date(filteredParams.start_date);
        if (!isNaN(date.getTime())) {
          filteredParams.start_date = date.toISOString().split('T')[0];
        }
      }
    }
    
    if (filteredParams.end_date) {
      // 将日期对象转换为ISO字符串格式，然后只取日期部分
      if (typeof filteredParams.end_date === 'object' && filteredParams.end_date instanceof Date) {
        filteredParams.end_date = filteredParams.end_date.toISOString().split('T')[0];
      } else if (typeof filteredParams.end_date === 'string') {
        // 如果已经是字符串，确保格式正确
        const date = new Date(filteredParams.end_date);
        if (!isNaN(date.getTime())) {
          filteredParams.end_date = date.toISOString().split('T')[0];
        }
      }
    }
    
    console.log('处理后的API参数:', filteredParams);
    
    const projectRes = await projectApi.getProjects(filteredParams);
    const projects = projectRes.items;
    
    // 计算总数
    totalProjects.value = projects.length;
    totalBudget.value = projects.reduce((sum, item) => sum + (item.budget || 0), 0);
    ongoingProjects.value = projects.filter(p => p.status === 'ongoing').length;
    completedProjects.value = projects.filter(p => p.status === 'completed').length;
    
    // 获取所有项目负责人的ID
    const leaderIds = [...new Set(projects.map(p => p.leader_id).filter(id => id))];
    
    // 加载所有负责人的详细信息，包含部门和团队信息
    if (leaderIds.length > 0) {
      try {
        // 获取所有员工数据（这里可以根据实际API设计进行调整）
        const allStaffs = await staffApi.getStaffs('', undefined, undefined, undefined, 1, 1000);
        allStaffs.forEach(staff => {
          staffMap.value.set(staff.id, staff);
        });
      } catch (error) {
        console.warn('Failed to load staff details:', error);
      }
    }
    
    // 按维度分组统计
    const groupedStats: Record<string, any> = {};
    
    projects.forEach(project => {
      let groupKey = '';
      let groupName = '';
      
      switch (filterForm.value.dimension) {
        case 'department':
          // 使用真实的部门信息
          if (project.leader_id && staffMap.value.has(project.leader_id)) {
            const staff = staffMap.value.get(project.leader_id)!;
            if (staff.department_id && staff.department_name) {
              groupKey = `dept_${staff.department_id}`;
              groupName = staff.department_name;
            } else {
              // 如果没有部门信息，使用未知部门
              groupKey = 'dept_unknown';
              groupName = '未知部门';
            }
          } else {
            // 如果没有负责人或负责人信息获取失败，使用未知部门
            groupKey = 'dept_unknown';
            groupName = '未知部门';
          }
          break;
        case 'team':
          // 使用真实的团队信息
          if (project.leader_id && staffMap.value.has(project.leader_id)) {
            const staff = staffMap.value.get(project.leader_id)!;
            if (staff.team_id && staff.team_name) {
              groupKey = `team_${staff.team_id}`;
              groupName = staff.team_name;
            } else {
              // 如果没有团队信息，使用未知团队
              groupKey = 'team_unknown';
              groupName = '未知团队';
            }
          } else {
            // 如果没有负责人或负责人信息获取失败，使用未知团队
            groupKey = 'team_unknown';
            groupName = '未知团队';
          }
          break;
        case 'leader':
          // 保留原有的负责人逻辑
          groupKey = project.leader_id?.toString() || 'unknown';
          groupName = project.leader_name || '未知负责人';
          break;
        case 'year':
          // 保留原有的年份逻辑
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

    console.log('chartData', chartData.value);
    
    // 确保DOM已经渲染完成再调用renderCharts
    await nextTick();
    // 增加延迟时间以确保DOM元素完全渲染并计算好尺寸
    setTimeout(() => {
      renderCharts();
    }, 500); // 增加延迟时间从300ms到500ms，确保DOM完全稳定
  } catch (error) {
    ElMessage.error('加载统计数据失败');
    console.error('Failed to load stats:', error);
  } finally {
    loading.value = false;
  }
};

// 监听维度变化
watch(() => filterForm.value.dimension, (newDimension, oldDimension) => {
  console.log(`维度从 ${oldDimension} 切换到 ${newDimension}`);
  
  // 销毁现有图表实例
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  if (budgetChartInstance) {
    budgetChartInstance.dispose();
    budgetChartInstance = null;
  }
  
  // 清空图表数据
  chartData.value = [];
  
  // 重新加载数据
  loadStats();
}, { immediate: false });

// 生命周期
onMounted(() => {
  loadChoices();
  // 增加延迟时间确保组件完全挂载
  setTimeout(() => {
    console.log('组件挂载完成，开始加载统计数据...');
    loadStats();
  }, 800); // 从500ms增加到800ms，确保组件完全挂载
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

onUnmounted(cleanup);

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    dimension: 'department',
    status: '',
    category_id: '',
    start_date: '',
    end_date: ''
  };
  // 销毁现有图表实例
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  if (budgetChartInstance) {
    budgetChartInstance.dispose();
    budgetChartInstance = null;
  }
  
  // 清空图表数据
  chartData.value = [];
  
  // 重新加载数据
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

// 模拟组件卸载时的清理
// 实际项目中应该在组件的unmounted钩子中调用

onUnmounted(cleanup);
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

/* 确保图表卡片有足够的空间 */
.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 20px 0;
  min-height: 450px;
  width: 100%;
}

.chart-card {
  height: 450px;
  overflow: visible;
  width: 100%;
  min-width: 300px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 增强图表容器样式 */
.chart-wrapper {
  width: 100% !important;
  height: calc(100% - 50px);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-height: 400px;
  position: relative;
  overflow: hidden;
}

.chart {
  width: 100% !important;
  height: 100% !important;
  min-height: 400px !important;
  min-width: 100% !important;
  display: block !important;
  position: relative !important;
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