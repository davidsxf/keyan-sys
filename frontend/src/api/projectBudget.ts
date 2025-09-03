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
  
  // 获取项目预算列表
  getProjectBudgets: async (params?: ProjectBudgetFilter): Promise<{ items: ProjectBudget[]; total: number }> => {
    const response = await http.get(`${API_BASE}/budgets`, { params });
    return response;
  },
  
  // 获取单个项目预算
  getProjectBudget: async (id: number): Promise<ProjectBudget> => {
    return await http.get(`${API_BASE}/budgets/${id}`);
  },
  
  // 创建项目预算
  createProjectBudget: async (data: ProjectBudgetForm): Promise<ProjectBudget> => {
    return await http.post(`${API_BASE}/budgets`, { data });
  },
  
  // 更新项目预算
  updateProjectBudget: async (id: number, data: ProjectBudgetForm): Promise<ProjectBudget> => {
    return await http.post(`${API_BASE}/budgets/${id}`, { data }, { method: 'PUT' });
  },
  
  // 删除项目预算
  deleteProjectBudget: async (id: number): Promise<void> => {
    await http.post(`${API_BASE}/budgets/${id}`, {}, { method: 'DELETE' });
  },
  
  // 获取预算类型选项
  getBudgetTypeChoices: async (): Promise<Choice[]> => {
    return await http.get(`${API_BASE}/types`);
  },
};