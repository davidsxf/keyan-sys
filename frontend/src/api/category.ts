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
  async getCategories(): Promise<Category[]> {
    const response = await fetch(`${API_BASE}/categories/`)
    return response.json()
  },

  // 创建分类
  async createCategory(data: CategoryForm): Promise<{ id: number }> {
    const response = await fetch(`${API_BASE}/categories/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return response.json()
  },

  // 更新分类
  async updateCategory(id: number, data: CategoryForm): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/categories/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return response.json()
  },

  // 删除分类
  async deleteCategory(id: number): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/categories/${id}/`, {
      method: 'DELETE'
    })
    return response.json()
  }
}