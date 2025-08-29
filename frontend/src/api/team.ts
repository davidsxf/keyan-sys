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


const API_BASE = '/api/v1/users';


export const teamApi = {
  // 获取团队列表
  async getTeams(search?: string, departmentId?: number, page = 1, limit = 10): Promise<Team[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (departmentId) params.append('department_id', String(departmentId));
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    
    const response = await fetch(`${API_BASE}/teams/?${params}`);
    if (!response.ok) throw new Error('获取团队列表失败');
    return response.json();
  },


  // 获取团队详情
  async getTeam(id: number): Promise<Team> {
    const response = await fetch(`${API_BASE}/teams/${id}/`);
    if (!response.ok) throw new Error('获取团队详情失败');
    return response.json();
  },


  // 创建团队
  async createTeam(data: TeamForm): Promise<Team> {
    const response = await fetch(`${API_BASE}/teams/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    if (!response.ok) throw new Error('创建团队失败');
    return response.json();
  },


  // 更新团队
  async updateTeam(id: number, data: TeamForm): Promise<Team> {
    const response = await fetch(`${API_BASE}/teams/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    if (!response.ok) throw new Error('更新团队失败');
    return response.json();
  },


  // 删除团队
  async deleteTeam(id: number): Promise<void> {
    const response = await fetch(`${API_BASE}/teams/${id}/`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('删除团队失败');
  }
};


// 部门相关API
export const departmentApi = {
  // 获取部门列表（用于下拉选择）
  async getDepartments(): Promise<DepartmentOption[]> {
    const response = await fetch(`${API_BASE}/departments/`);
    if (!response.ok) throw new Error('获取部门列表失败');
    return response.json();
  }
};
