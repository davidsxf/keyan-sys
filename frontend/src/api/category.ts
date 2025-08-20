import { http } from "@/utils/http";

// 分类数据类型定义
interface Category {  
  id?: number;  
  name: string;  
  parent?: number | null;  
  weight?: number;  
  sort_order?: number;  
  created_at?: string;  
  updated_at?: string;  
  children?: Category[];  
}

// 分类API响应类型
export interface CategoryResponse {
  success: boolean;
  data: Category[];
}

// 单个分类API响应类型
export interface SingleCategoryResponse {
  success: boolean;
  data: Category;
}

// 获取所有分类
export const getCategories = () => {
  console.log("获取所有分类");
  return http.get<CategoryResponse>("/api/v1/core/categories");

};

// 获取单个分类
// 添加错误处理示例
export const getCategoriesWithErrorHandling = () => {
  return http.get<CategoryResponse>("/api/categories/")
    .catch(error => {
      console.error("获取分类数据失败:", error);
      // 可以添加重试逻辑或返回默认数据
      return { success: false, data: [] };
    });
}

// 获取单个分类
export const getCategory = (id: number) => {
  return http.get<SingleCategoryResponse>(`/api/categories/${id}/`);
};

// 创建分类
export const createCategory = (data: Category) => {
  return http.post<SingleCategoryResponse>("/api/categories/", data);
};

// 更新分类
export const updateCategory = (id: number, data: Category) => {
  return http.request<SingleCategoryResponse>("put", `/api/categories/${id}/`, { data });
};

// 删除分类
export const deleteCategory = (id: number) => {
  return http.request<{ success: boolean }>("delete", `/api/categories/${id}/`);
};