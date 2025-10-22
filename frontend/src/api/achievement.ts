// 期刊信息接口
export interface Journal {
  id: number;
  name: string;
  issn: string;
  jcr_quartile?: string;
  impact_factor?: number;
  created_at: string;
  updated_at: string;
}

// 期刊表单接口
export interface JournalForm {
  name: string;
  issn: string;
  jcr_quartile?: string;
  impact_factor?: number;
}

// 期刊过滤条件接口
export interface JournalFilter {
  name?: string;
  issn?: string;
  jcr_quartile?: string;
  min_impact_factor?: number;
}

// 作者信息接口
export interface Author {
  id: number;
  name: string;
  email?: string;
  staff_id?: number;
  staff_name?: string;
  external_organization?: string;
  created_at: string;
  updated_at: string;
}

// 作者表单接口
export interface AuthorForm {
  name: string;
  email?: string;
  staff_id?: number;
  external_organization?: string;
}

// 论文信息接口
export interface Paper {
  id: number;
  title: string;
  first_authors: Author[];
  corresponding_authors: Author[];
  journal?: Journal;
  publication_year: number;
  unit_ranking: number;
  page_numbers?: string;
  keywords?: string;
  abstract?: string;
  created_at: string;
  updated_at: string;
}

// 论文表单接口
export interface PaperForm {
  title: string;
  first_author_ids: number[];
  corresponding_author_ids: number[];
  journal_id?: number;
  publication_year: number;
  unit_ranking: number;
  page_numbers?: string;
  keywords?: string;
  abstract?: string;
}

import { http } from '@/utils/http';
const API_BASE = '/api/v1/achievement';

export const achievementApi = {
  // 期刊相关API
  // 获取期刊列表
  getJournals: async (params?: JournalFilter): Promise<Journal[]> => {
    try {
      const response = await http.get(`${API_BASE}/journals/`, { params });
      return response;
    } catch (error) {
      console.error('获取期刊列表失败:', error);
      throw error;
    }
  },

  // 获取单个期刊
  getJournal: async (id: number): Promise<Journal> => {
    try {
      const response = await http.get(`${API_BASE}/journals/${id}/`);
      return response;
    } catch (error) {
      console.error(`获取期刊 ${id} 详情失败:`, error);
      throw error;
    }
  },

  // 创建期刊
  createJournal: async (data: JournalForm): Promise<Journal> => {
    try {
      const response = await http.post(`${API_BASE}/journals/`, { data });
      return response;
    } catch (error) {
      console.error('创建期刊失败:', error);
      throw error;
    }
  },

  // 更新期刊
  updateJournal: async (id: number, data: JournalForm): Promise<Journal> => {
    try {
      const response = await http.post(`${API_BASE}/journals/${id}/`, { data }, { method: 'PUT' });
      return response;
    } catch (error) {
      console.error(`更新期刊 ${id} 失败:`, error);
      throw error;
    }
  },

  // 删除期刊
  deleteJournal: async (id: number): Promise<void> => {
    try {
      await http.post(`${API_BASE}/journals/${id}/`, {}, { method: 'DELETE' });
    } catch (error) {
      console.error(`删除期刊 ${id} 失败:`, error);
      throw error;
    }
  },

  // 作者相关API
  // 获取作者列表
  getAuthors: async (params?: any): Promise<Author[]> => {
    try {
      // 构建符合后端期望的参数格式
      const requestParams: any = {};
      
      // 添加分页参数和过滤参数（直接作为顶级参数）
      if (params) {
        // 添加分页参数
        if (params.skip !== undefined) requestParams.skip = params.skip;
        if (params.limit !== undefined) requestParams.limit = params.limit;
        
        // 直接将过滤参数添加为顶级参数，以匹配后端处理逻辑
        if (params.name !== undefined) requestParams.name = params.name;
        if (params.email !== undefined) requestParams.email = params.email;
        if (params.has_staff !== undefined) requestParams.has_staff = params.has_staff;
        if (params.external_organization !== undefined) requestParams.external_organization = params.external_organization;
        
        // 兼容可能存在的filters对象格式
        if (params.filters && typeof params.filters === 'object') {
          if (params.filters.name !== undefined) requestParams.name = params.filters.name;
          if (params.filters.email !== undefined) requestParams.email = params.filters.email;
          if (params.filters.has_staff !== undefined) requestParams.has_staff = params.filters.has_staff;
          if (params.filters.external_organization !== undefined) requestParams.external_organization = params.filters.external_organization;
        }
      }

      console.log('发送的API参数:', requestParams);
      return await http.get(`${API_BASE}/authors/`, { params: requestParams });
    } catch (error) {
      console.error('获取作者列表失败:', error);
      throw error;
    }
  },

  // 获取单个作者
  getAuthor: async (id: number): Promise<Author> => {
    try {
      const response = await http.get(`${API_BASE}/authors/${id}/`);
      return response;
    } catch (error) {
      console.error(`获取作者 ${id} 详情失败:`, error);
      throw error;
    }
  },

  // 创建作者
  createAuthor: async (data: AuthorForm): Promise<Author> => {
    try {
      const response = await http.post(`${API_BASE}/authors/`, { data });
      return response;
    } catch (error) {
      console.error('创建作者失败:', error);
      throw error;
    }
  },

  // 更新作者
  updateAuthor: async (id: number, data: AuthorForm): Promise<Author> => {
    try {
      const response = await http.post(`${API_BASE}/authors/${id}/`, { data }, { method: 'PUT' });
      return response;
    } catch (error) {
      console.error(`更新作者 ${id} 失败:`, error);
      throw error;
    }
  },

  // 删除作者
  deleteAuthor: async (id: number): Promise<void> => {
    try {
      await http.post(`${API_BASE}/authors/${id}/`, {}, { method: 'DELETE' });
    } catch (error) {
      console.error(`删除作者 ${id} 失败:`, error);
      throw error;
    }
  },

  // 论文相关API
  // 获取论文列表
  getPapers: async (): Promise<Paper[]> => {
    try {
      const response = await http.get(`${API_BASE}/papers/`);
      return response;
    } catch (error) {
      console.error('获取论文列表失败:', error);
      throw error;
    }
  }
};