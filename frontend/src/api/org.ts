export interface Org {
  id: number;
  name: string;
  description?: string;
  phone?: string;
  email?: string;
  org_type?: string;
  created_at: string;
  updated_at: string;
}


export interface OrgForm {
  name: string;
  description?: string;
  phone?: string;
  email?: string;
  org_type?: string;
}


// import { Org, OrgForm, ApiResponse } from '@/types/org';


const API_BASE = '/api/v1/core';


export const orgApi = {
  // 获取组织列表
  async getOrgs(search?: string, page = 1, limit = 10): Promise<Org[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    
    const response = await fetch(`${API_BASE}/orgs/?${params}`);
    if (!response.ok) throw new Error('获取组织列表失败');
    return response.json();
  },


  // 获取组织详情
  async getOrg(id: number): Promise<Org> {
    const response = await fetch(`${API_BASE}/orgs/${id}/`);
    if (!response.ok) throw new Error('获取组织详情失败');
    return response.json();
  },


  // 创建组织
  async createOrg(data: OrgForm): Promise<Org> {
    const response = await fetch(`${API_BASE}/orgs/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    if (!response.ok) throw new Error('创建组织失败');
    return response.json();
  },


  // 更新组织
  async updateOrg(id: number, data: OrgForm): Promise<Org> {
    const response = await fetch(`${API_BASE}/orgs/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    if (!response.ok) throw new Error('更新组织失败');
    return response.json();
  },


  // 删除组织
  async deleteOrg(id: number): Promise<void> {
    const response = await fetch(`${API_BASE}/orgs/${id}/`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('删除组织失败');
  }
};
