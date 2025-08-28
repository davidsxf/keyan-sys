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

import { Department, DepartmentForm } from '@/api/department';

const API_BASE = '/api/v1/users';

export const departmentApi = {
  // 获取部门树
  async getDepartments(): Promise<Department[]> {
    const response = await fetch(`${API_BASE}/departments/`);
    if (!response.ok) throw new Error('获取部门列表失败');
    return response.json();
  },

  // 创建部门
  async createDepartment(data: DepartmentForm): Promise<Department> {
    const response = await fetch(`${API_BASE}/departments/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || '创建部门失败');
    }
    
    return response.json();
  },

  // 更新部门
  async updateDepartment(id: number, data: DepartmentForm): Promise<Department> {
    const response = await fetch(`${API_BASE}/departments/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || '更新部门失败');
    }
    
    return response.json();
  },

  // 删除部门
  async deleteDepartment(id: number): Promise<void> {
    const response = await fetch(`${API_BASE}/departments/${id}/`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('删除部门失败');
  }
};