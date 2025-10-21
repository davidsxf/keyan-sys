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
      // 旧代码
      // 构建请求参数对象
      const requestParams: any = {};
      
      // 提取分页参数
      if (params) {
        if (params.skip !== undefined) requestParams.skip = params.skip;
        if (params.limit !== undefined) requestParams.limit = params.limit;
        if (params.page !== undefined) requestParams.page = params.page;
        if (params.page_size !== undefined) requestParams.page_size = params.page_size;
        
        // 将过滤参数放入filters对象中
        const filters: any = {};
        if (params.name !== undefined) filters.name = params.name;
        // ...其他过滤参数
        
        // 只有当filters对象不为空时才添加到请求参数中
        if (Object.keys(filters).length > 0) {
          requestParams.filters = filters;
        }
      }
      
      // 新代码
      // 直接使用params对象，不进行额外封装
      // 这样所有参数（包括name等过滤条件）都会直接作为查询参数传递
      console.log('直接传递的请求参数:', params); // 添加日志记录传递的请求参数
      const response = await http.get(`${API_BASE}/authors/`, { params });
      return response;
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