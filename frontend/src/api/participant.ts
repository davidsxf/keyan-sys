export interface ProjectStaff {
  id: number;
  project_id: number;
  project_title?: string;
  staff_id: number;
  staff_name?: string;
  staff_department?: string;
  role: string;
  role_display?: string;
  order?: number;
  join_date?: string;
  leave_date?: string;
  remark?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectStaffForm {
  project_id: number;
  staff_id: number;
  role: string;
  order?: number;
  join_date?: string;
  leave_date?: string;
  remark?: string;
}

export interface ProjectStaffFilter {
  project_id?: number;
  staff_id?: number;
  staff_name?: string;
  role?: string;
}

export interface Choice {
  value: string;
  label: string;
}

export interface Project {
  id: number;
  title: string;
  number: string;
  funding_number?: string;
  leader_id?: number;
  leader_name?: string;
  start_date?: string;
  end_date?: string;
  status: string;
  status_display: string;
  category_id?: number;
  category_name?: string;
  type?: string;
  type_name?: string;
  budget?: number;
  research_area?: string;
  source_id?: number;
  source_name?: string;
  undertake: string;
  undertake_display: string;
  remark?: string;
  created_at: string;
  updated_at: string;
}

import { http } from '@/utils/http';
const API_BASE = '/api/v1/projects';

// 注意：根据后端路由结构，这里已经包含了 /projects 前缀
// 所以后面的路由不要重复添加 /projects

export const participantApi = {
  // 获取项目参与人员列表
  getParticipants: async (params?: ProjectStaffFilter): Promise<{ items: ProjectStaff[]; total: number; }> => {
    const response = await http.get(`${API_BASE}/participants/list`, { params });
    return response;
  },

  // 获取项目参与人员角色选项
  getParticipantRoles: async (): Promise<Choice[]> => {
    return await http.get(`${API_BASE}/participants/roles`);
  },

  // 创建项目参与人员
  createParticipant: async (data: ProjectStaffForm): Promise<ProjectStaff> => {
    console.log('createParticipant data:', data);
    return await http.post(`${API_BASE}/participants/create`, { data });
  },

  // 获取单个项目参与人员详情
  getParticipant: async (id: number): Promise<ProjectStaff> => {
    return await http.get(`${API_BASE}/participants/${id}`);
  },

  // 获取参与人员参与的项目列表
  getParticipantProjects: async (participantId: number): Promise<Project[]> => {
    return await http.get(`${API_BASE}/participants/${participantId}/projects`);
  },

  // 更新项目参与人员信息
  updateParticipant: async (id: number, data: ProjectStaffForm): Promise<ProjectStaff> => {
    return await http.post(`${API_BASE}/participants/${id}`, { data }, { method: 'PUT' });
  },

  // 删除项目参与人员
  deleteParticipant: async (id: number): Promise<{ success: boolean; message: string }> => {
    return await http.post(`${API_BASE}/participants/${id}`, {}, { method: 'DELETE' });
  },

  // 获取指定项目的所有参与人员
  getProjectParticipants: async (projectId: number): Promise<{ items: ProjectStaff[]; total: number; }> => {
    console.log('getProjectParticipants projectId:', projectId);
    const response = await http.get(`${API_BASE}/${projectId}/participants`);
    return response;
  },
};