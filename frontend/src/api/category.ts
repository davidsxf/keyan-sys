import { http } from "@/utils/http";

// 分类数据类型定义
interface Category {  
  id?: number | null;   
  name: string;  
  parent?: number ;  
  weight?: number ;  
  sort_order?: number;  
  // created_at?: string;  
  // updated_at?: string;  
  // children?: Category[];  
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
  
  return http.get<CategoryResponse>("/api/v1/core/categories")
    .then(response => {
      // console.log("获取分类:", response);
      return { data: response, success: true };
    })
    .catch(error => {
      // console.error("获取分类数据失败:", error);
      // 可以添加重试逻辑或返回默认数据
      return { success: false, data: [] };
    });
};

// 获取单个分类
// 添加错误处理示例
// export const getCategoriesWithErrorHandling = () => {
//   return http.get<CategoryResponse>("/api/categories/")
//     .catch(error => {
//       console.error("获取分类数据失败:", error);
//       // 可以添加重试逻辑或返回默认数据
//       return { success: false, data: [] };
//     });
// }

// 获取单个分类
export const getCategory = (id: number) => {
  return http.get<SingleCategoryResponse>(`/api/v1/core/categories/${id}`);
};

// 创建分类
export const createCategory = (data: Category) => {
  // 处理parent_id
  if (data.parent === 0 || data.parent === null) {
    data.parent = null;
  }
  // 加个测试
  //{id: undefined, name: '333', parent_id: 1, weight: 0, sort_order: 0}
// 测试数据示例
// const testData: Category = { id: undefined, name: '333', parent: 1, weight: 0, sort_order: 0 };
//   console.log("创建分类cat:", testData);
  return http.post<SingleCategoryResponse>("/api/v1/core/categories", data);
};

// 更新分类
export const updateCategory = (id: number, data: Category) => {
  // console.log("更新分类cat:", data);
  return http.request<SingleCategoryResponse>("put", `/api/v1/core/categories/${id}`, { data });
};

// 删除分类
export const deleteCategory = (id: number) => {
  return http.request<{ success: boolean }>("delete", `/api/v1/core/categories/${id}`);
};