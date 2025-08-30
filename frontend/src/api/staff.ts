export enum StaffStatus {
  ON_DUTY = "在职",
  OFF_DUTY = "离职",
  RETIRE = "退休"
}

export interface Staff {
  id: number;
  name: string;
  gender?: string;
  birthday?: string;
  email?: string;
  entry_date?: string;
  department_id?: number;
  department_name?: string;
  team_id?: number;
  team_name?: string;
  position?: string;
  is_team_leader: boolean;
  status: StaffStatus;
  phone?: string;
  remark?: string;
  created_at: string;
  updated_at: string;
}

export interface StaffForm {
  name: string;
  gender?: string;
  birthday?: string;
  email?: string;
  entry_date?: string;
  department_id?: number | null;
  team_id?: number | null;
  position?: string;
  is_team_leader: boolean;
  status: StaffStatus;
  phone?: string;
  remark?: string;
}

export interface DepartmentOption {
  id: number;
  name: string;
}

export interface TeamOption {
  id: number;
  name: string;
}

import { http }  from '@/utils/http';

const API_BASE = '/api/v1/users';

export const staffApi = {
  // 获取员工列表
  async getStaffs(
    search?: string, 
    departmentId?: number, 
    teamId?: number, 
    status?: StaffStatus, 
    page = 1, 
    limit = 10
  ): Promise<Staff[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (departmentId) params.append('department_id', String(departmentId));
    if (teamId) params.append('team_id', String(teamId));
    if (status) params.append('status', status);
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    
    const response = await http.get(`${API_BASE}/staffs/?${params}`)
    return response;
  },

  // 获取员工详情
  async getStaff(id: number): Promise<Staff> {
    const response = await http.get(`${API_BASE}/staffs/${id}/`);
    return response;
  },

  // 创建员工
  async createStaff(data: StaffForm): Promise<Staff> {
    const response = await http.post(`${API_BASE}/staffs/`, { data:data });
    return response;
  },

  // 更新员工
  async updateStaff(id: number, data: StaffForm): Promise<Staff> {
    const response = await http.post(`${API_BASE}/staffs/${id}/`, { data:data },{ method: 'PUT' });
    return response;
  },

  // 删除员工
  async deleteStaff(id: number): Promise<void> {
    const response = await http.post(`${API_BASE}/staffs/${id}/`,{}, {
      method: 'DELETE'
    });
    return response;

  }
};

export const departmentApi = {
  // 获取部门选项
  async getDepartmentOptions(): Promise<DepartmentOption[]> {
    const response = await http.get(`${API_BASE}/departments/options/`);
    
    return response;
  }
};

export const teamApi = {
  // 获取团队选项
  async getTeamOptions(): Promise<TeamOption[]> {
    const response = await http.get(`${API_BASE}/teams/options/`);
    
    return response;
  }
};

