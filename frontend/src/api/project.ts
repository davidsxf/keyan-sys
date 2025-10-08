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
  level?: string;
  level_name?: string;
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


export interface ProjectForm {
  title: string;
  number: string;
  funding_number?: string;
  leader_id?: number;
  start_date?: string;
  end_date?: string;
  status: string;
  level?: string;
  category_id?: number;
  type?: string;
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
  level?: string;
  category_id?: number;
  type?: string;
  leader_id?: number;
  undertake?: string;
  source?: string; // 从 number 改为 string
  start_date?: string; // 添加缺失的字段
  end_date?: string; // 添加缺失的字段
}


export interface Choice {
  value: string;
  label: string;
}

export interface ProjectLeaderChange {
  id: number;
  project_id: number;
  project_title: string;
  leader_id: number;
  leader_name: string;
  change_date: string;
  remark?: string;
  created_at: string;
  updated_at: string;

}


import { http } from '@/utils/http';
const API_BASE = '/api/v1/projects';

// 注意：根据后端路由结构，这里已经包含了 /projects 前缀
// 所以后面的路由不要重复添加 /projects

export const projectApi = {
  // 获取项目列表
  getProjects: async (params?: ProjectFilter): Promise<{ items: Project[]; total: number; }> => {
    // 修复参数传递方式，GET参数直接作为第二个参数
    // console.log('paramsf', params);
    const response = await http.get(API_BASE,{params});

    return response;
  },

  // 获取单个项目
  getProject: async (id: number): Promise<Project> => {
    // 统一使用 http 工具
    return await http.get(`${API_BASE}/${id}`);
  },

  // 创建项目
  createProject: async (data: ProjectForm): Promise<Project> => {
    // 统一使用 http 工具
    return await http.post(API_BASE, { data });
  },

  // 更新项目
  updateProject: async (id: number, data: ProjectForm): Promise<Project> => {
    // 统一使用 http 工具
    return await http.post(`${API_BASE}/${id}`, { data }, { method: 'PUT' });
  },

  // 删除项目
  deleteProject: async (id: number): Promise<void> => {
    // 修复 URL 路径，移除重复的 /projects
    await http.post(`${API_BASE}/${id}`, {}, { method: 'DELETE' });
  },


//获取项目级别
getLevelChoices: async (): Promise<Choice[]> => {
  return await http.get(`${API_BASE}/level/choices`);
},

  // 获取状态选项
  getStatusChoices: async (): Promise<Choice[]> => {
    // 统一使用 http 工具，修复 URL 路径
    return await http.get(`${API_BASE}/status/choices`);
  },

  // 获取承担方式选项
  getUndertakeChoices: async (): Promise<Choice[]> => {
    // 统一使用 http 工具，修复 URL 路径
    return await http.get(`${API_BASE}/undertake/choices`);
  },

  // 获取类别选项
  getCategoryChoices: async (): Promise<Choice[]> => {
    // 注意：后端实际提供的是 type/choices 接口
    return await http.get(`${API_BASE}/category/choices`);
  },
  
  // 获取负责人选项
  getLeaderChoices: async (): Promise<Choice[]> => {
    // 调用新的 API 接口获取负责人列表
    return await http.get('/api/v1/users/staffs/choices');
  },
  // 获取类型选项
  getTypeChoices: async (): Promise<Choice[]> => {
    // 统一使用 http 工具，修复 URL 路径
    return await http.get(`${API_BASE}/type/choices`);
  },

  // 获取项目来源选项
  getSourceChoices: async (): Promise<Choice[]> => {
    return await http.get(`${API_BASE}/source/choices`);
  },

  // 获取项目负责人变更记录
/**
   * 获取项目负责人变更记录
   * @param projectId 项目ID
   * @returns 包含变更记录和总数的对象
   */
  getProjectLeaderChanges: async (projectId: number): Promise<{ items: any[], count: number }> => {
    const response = await http.get(`${API_BASE}/${projectId}/leader-changes`);
    console.log("leader changes response:", response);
    // 确保返回的数据格式符合前端期望
    if (response && Array.isArray(response)) {
      // 处理直接返回数组的情况
      return { items: response, count: response.length };
    } else if (response && typeof response === 'object') {
      // 处理返回对象的情况，优先查找items和count字段
      if ('items' in response && 'count' in response) {
        return response;
      }
      // 兼容可能的其他格式
      else if ('results' in response && 'count' in response) {
        return { items: response.results, count: response.count };
      }
    }
    // 默认返回空数组和0计数
    return { items: [], count: 0 };
  },

  // 在projectApi对象中添加创建项目负责人变更记录的方法
  createProjectLeaderChange: async (data: any): Promise<any> => {
    return await http.post(`${API_BASE}/leader-change`, { data });
  },
};








