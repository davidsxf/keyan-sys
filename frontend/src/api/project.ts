// types/project.ts
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
  type_id?: number;
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


export interface ProjectForm {
  title: string;
  number: string;
  funding_number?: string;
  leader_id?: number;
  start_date?: string;
  end_date?: string;
  status: string;
  type_id?: number;
  budget?: number;
  research_area?: string;
  source_id?: number;
  undertake: string;
  remark?: string;
}


export interface ProjectFilter {
  title?: string;
  number?: string;
  status?: string;
  type_id?: number;
  leader_id?: number;
  undertake?: string;
}


export interface Choice {
  value: string;
  label: string;
}






const API_BASE = '/api/v1/project';





export const projectApi = {
  // 获取项目列表
  getProjects: async (params?: ProjectFilter): Promise<{ items: Project[]; total: number }> => {
    const response = await fetch(`${API_BASE}/projects`, { params });
    return {
      items: (await response.json()).items,
      total: (await response.json()).total,
    };
  },


  // 获取单个项目
  getProject: async (id: number): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects/${id}`);
    return await response.json();   
  },


  // 创建项目
  createProject: async (data: ProjectForm): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return await response.json();
  },


  // 更新项目
  updateProject: async (id: number, data: ProjectForm): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    return await response.json();
  },


  // 删除项目
  deleteProject: async (id: number): Promise<void> => {
    await fetch(`${API_BASE}/projects/${id}`, {
      method: 'DELETE',
    });
  },


  // 获取状态选项
  getStatusChoices: async (): Promise<Choice[]> => {
    const response = await fetch(`${API_BASE}/projects/status/choices`);
    return await response.json();
  },


  // 获取承担方式选项
  getUndertakeChoices: async (): Promise<Choice[]> => {
    const response = await fetch(`${API_BASE}/projects/undertake/choices`);
    return await response.json();
  },
};
