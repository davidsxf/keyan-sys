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


export const teamApi = {
  // 获取团队列表
  async getTeams(search?: string, departmentId?: number, page = 1, limit = 10): Promise<Team[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (departmentId) params.append('department_id', String(departmentId));
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    
    const response = await http.get(`${API_BASE}/teams/?${params}`);

    return response;
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


