import { http } from "@/utils/http";

export interface Category {
  id: number
  name: string
  parent_id?: number | null
  weight: number
  sort_order: number
  children?: Category[]
}

export interface CategoryForm {
  name: string
  parent_id?: number | null
  weight: number
  sort_order: number
}

const API_BASE = '/api/v1/core'

export const categoryApi = {
  // 获取分类树
  async getCategories(search?: string, page = 1, limit = 10): Promise<{data: Category[], total: number}> {
    const params = new URLSearchParams();
    params.append('skip', String((page - 1) * limit));
    params.append('limit', String(limit));
    if (search) {
      params.append('search', search);
    }
  
    const response = await http.get(`${API_BASE}/categories/?${params}`)
    return response
  },

  // 创建分类
  async createCategory(data: CategoryForm): Promise<{ id: number }> {
    return await http.post(`${API_BASE}/categories/`, { data: data })
  },

  // 更新分类
  async updateCategory(id: number, data: CategoryForm): Promise<{ success: boolean }> {
    return await http.post(`${API_BASE}/categories/${id}/`, { data: data }, { method: 'PUT' })
  },

  // 删除分类
  async deleteCategory(id: number): Promise<{ success: boolean }> {
    return await http.post(`${API_BASE}/categories/${id}/`, {}, { method: 'DELETE' })
  }
}