export interface Team {
  id: number;
  name: string;
  description?: string;
  department_id?: number;
  department_name?: string;
  created_at: string;
  updated_at: string;
}


export interface TeamForm {
  name: string;
  description?: string;
  department_id?: number | null;
}


export interface DepartmentOption {
  id: number;
  name: string;
}

import { http } from '@/utils/http';

const API_BASE = '/api/v1/users';


// 定义分页响应接口
interface PaginationResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

// 更新团队 API
export const teamApi = {
  // 获取团队列表
  async getTeams(search?: string, departmentId?: number, page = 1, limit = 10): Promise<{data: Team[], total: number}> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (departmentId) params.append('department_id', String(departmentId));
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    
    const response = await http.get(`${API_BASE}/teams/?${params}`);
    
    // 处理可能的分页响应格式
    if (response && response.data && typeof response.total === 'number') {
      // 格式1: { data: [...], total: 100 }
      return {
        data: response.data,
        total: response.total
      };
    } else if (response && Array.isArray(response)) {
      // 格式2: 直接返回数组，这种情况下无法获取总条数
      // 为了演示，这里返回一个默认值，实际应该根据后端API调整
      return {
        data: response,
        total: 0 // 实际应该从响应头或其他地方获取
      };
    } else if (response && response.results && typeof response.count === 'number') {
      // 格式3: Django REST framework 默认格式 { results: [...], count: 100 }
      return {
        data: response.results,
        total: response.count
      };
    }
    
    // 默认返回
    return {
      data: [],
      total: 0
    };
  },


  // 获取团队详情
  async getTeam(id: number): Promise<Team> {
    const response = await http.get(`${API_BASE}/teams/${id}/`);
    return response;
  },


  // 创建团队
  async createTeam(data: TeamForm): Promise<Team> {
    const response = await http.post(`${API_BASE}/teams/`, { data: data });
    return response;
  },


  // 更新团队
  async updateTeam(id: number, data: TeamForm): Promise<Team> {
    const response = await http.post(`${API_BASE}/teams/${id}/`, { data: data }, { method: 'PUT' });
    return response;
  },


  // 删除团队
  async deleteTeam(id: number): Promise<void> {
    const response = await http.post(`${API_BASE}/teams/${id}/`, {}, { method: 'DELETE' });
    return response;
  }
};


// 部门相关API
export const departmentApi = {
  // 获取部门选项列表（用于下拉选择）
  async getDepartmentOptions(): Promise<DepartmentOption[]> {
    const response = await http.get(`${API_BASE}/departments/options/`);

    return response;
  }
};


