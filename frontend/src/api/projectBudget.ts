// 项目预算类型定义

export interface ProjectBudget {
  id: number;
  project_id: number;
  project_title?: string;
  name: string;
  amount?: number;
  year?: number;
  type: string;
  type_display?: string;
  remark?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectBudgetForm {
  project_id: number;
  name: string;
  amount?: number;
  year?: number;
  type: string;
  remark?: string;
}

export interface ProjectBudgetFilter {
  project_id?: number;
  name?: string;
  type?: string;
  year?: number;
  start_date?: string;
  end_date?: string;
}

import { http } from '@/utils/http';
const API_BASE = '/api/v1/projects/budget';


export const projectBudgetApi = {
  // ... 现有项目相关方法 ...
  
  // 项目预算相关方法
  
  // 修改getProjectBudgets方法，统一调用后端正确的API端点
  getProjectBudgets: async (params?: ProjectBudgetFilter): Promise<{ items: ProjectBudget[]; total: number }> => {
    // 统一调用后端正确的API端点
    // 不再根据project_id参数切换端点，而是让后端根据project_id参数进行筛选
    return await http.get(`${API_BASE}/budgets`, { params });
  },
  
  // 获取单个项目预算
  getProjectBudget: async (id: number): Promise<{ results: ProjectBudget[] }> => {
    // console.log('获取项目预算:', id);
    return await http.get(`${API_BASE}/project/${id}`);
  },
  
  // 创建项目预算
  createProjectBudget: async (data: ProjectBudgetForm): Promise<ProjectBudget> => {
    return await http.post(`${API_BASE}/budgets`, { data });
  },
  
  // 更新项目预算
  updateProjectBudget: async (id: number, data: ProjectBudgetForm): Promise<ProjectBudget> => {
    // 直接传递数据对象，而不是包装在data属性中
    return await http.post(`${API_BASE}/${id}`, { data }, { method: 'PUT' });
  },

  // 删除项目预算
  deleteProjectBudget: async (id: number): Promise<void> => {
    // 同样修复删除请求，使用正确的DELETE请求方式
    return await http.request('delete', `${API_BASE}/budgets/${id}`);
  },
  
  // 获取预算类型选项
  getBudgetTypeChoices: async (): Promise<Choice[]> => {
    return await http.get(`${API_BASE}/types`);
  },
};