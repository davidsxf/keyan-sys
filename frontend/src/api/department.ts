export interface Department {
  id: number;
  name: string;
  description?: string;
  parent_id?: number;
  created_at: string;
  updated_at: string;
  children?: Department[]; // 用于树形结构
}

export interface DepartmentForm {
  name: string;
  description?: string;
  parent_id?: number | null;
}

import { http } from '@/utils/http';

import { Department, DepartmentForm } from '@/api/department';

const API_BASE = '/api/v1/users';

export const departmentApi = {
  // 获取部门树
  async getDepartments(): Promise<Department[]> {
    const response = await http.get(`${API_BASE}/departments/`);
    
    return response;
  },

  // 创建部门
  async createDepartment(data: DepartmentForm): Promise<Department> {
    const response = await http.post(`${API_BASE}/departments/`, { data: data });
    
    return response;
  },

  // 更新部门
  async updateDepartment(id: number, data: DepartmentForm): Promise<Department> {
    const response = await http.post(`${API_BASE}/departments/${id}/`, { data: data }, { method: 'PUT' });
    
    return response;
  },

  // 删除部门
  async deleteDepartment(id: number): Promise<void> {
    const response = await http.post(`${API_BASE}/departments/${id}/`, {}, { method: 'DELETE' });
    return response;
  }
};