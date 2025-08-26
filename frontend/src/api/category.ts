import { http } from "@/utils/http";

// 分类数据类型定义
export interface Category {
  id: number;
  name: string;
  parent: number | null;
  weight: number;
  sort_order: number;
  created_at?: string;
  updated_at?: string;
  has_children?: boolean;
  children?: Category[];
}

export interface CategoryFormData {
  name: string;
  parent: number | null;
  weight: number;
  sort_order: number;
}

export interface CategoryResponse {
  success: boolean;
  data?: Category | Category[];
  message?: string;
  errors?: Record<string, string[]>;
}

/**
 * 获取类别列表
 * @param parentId 可选，父类别ID，用于筛选子类别
 * @returns 类别列表数据，包含success字段
 */
export const getCategories = async (parentId?: number): Promise<CategoryResponse> => {
  // 构建查询参数
  const params = parentId !== undefined ? { parent: parentId } : {};
  
  try {
    // 调用后端API获取类别列表
    const response = await http.get<CategoryResponse>("/api/v1/core/categories", { params });
    // console.log("获取类别列表成功:", response);
    // 确保返回对象包含success字段
    if (response && typeof response === 'object') {
      if ('success' in response) {
        return response as CategoryResponse;
      } else {
        // 如果后端返回的响应没有success字段，手动添加
        return { success: true, data: response as Category | Category[] };
      }
    } else {
      // 如果响应不是对象，包装成标准格式
      return { success: true, data: response as Category | Category[] };
    }
  } catch (error) {
    console.log("获取类别列表失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};


// 获取单个类别详情
export const getCategory = async (id: number): Promise<CategoryResponse> => {
  try {
    const response = await http.get<CategoryResponse>(`/api/v1/core/categories/${id}`);
    // console.log("获取类别详情成功:", response);
    
    // 确保返回对象包含success字段
    if (response && typeof response === 'object') {
      if ('success' in response) {
        return response as CategoryResponse;
      } else {
        // 如果后端返回的响应没有success字段，手动添加
        return { success: true, data: response as Category };
      }
    } else {
      // 如果响应不是对象，包装成标准格式
      return { success: true, data: response as Category };
    }
  } catch (error) {
    console.log("获取类别详情失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};

// 创建新类别
export const createCategory = async (data: CategoryFormData): Promise<CategoryResponse> => {
  try {
    // 调用后端API创建新类别
    const response = await http.post<CategoryResponse>('/api/v1/core/categories', data);
    // console.log("创建类别成功:", response);
    
    // 确保返回对象包含success字段
    if (response && typeof response === 'object') {
      if ('success' in response) {
        return response as CategoryResponse;
      } else {
        // 如果后端返回的响应没有success字段，手动添加
        return { success: true, data: response as Category };
      }
    } else {
      // 如果响应不是对象，包装成标准格式
      return { success: true, data: response as Category };
    }
  } catch (error) {
    console.log("创建类别失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};

// 更新类别
export const updateCategory = async (id: number, data: CategoryFormData): Promise<CategoryResponse> => {
  try {
    // 调用后端API更新类别
    console.log('传入类别:', id, data);
    const response = await http.request<CategoryResponse>('PUT', `/api/v1/core/categories/${id}`, { data });
    console.log("更新类别成功:", response);
    
    // 确保返回对象包含success字段
    if (response && typeof response === 'object') {
      if ('success' in response) {
        return response as CategoryResponse;
      } else {
        // 如果后端返回的响应没有success字段，手动添加
        return { success: true, data: response as Category };
      }
    } else {
      // 如果响应不是对象，包装成标准格式
      return { success: true, data: response as Category };
    }
  } catch (error) {
    console.log("更新类别失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};

// 删除类别
export const deleteCategory = async (id: number): Promise<CategoryResponse> => {
  try {
    // 调用后端API删除类别
    await http.request<void>('DELETE', `/api/v1/core/categories/${id}`);
    // console.log("删除类别成功:", id);
    
    // 删除成功时返回success: true
    return { success: true };
  } catch (error) {
    console.log("删除类别失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};

// 获取所有顶级类别（用于下拉选择）
export const getTopLevelCategories = async (): Promise<CategoryResponse> => {
  try {
    // 调用getCategories函数获取顶级类别（parent为null）
    const response = await getCategories(null);
    return response;
  } catch (error) {
    console.log("获取顶级类别失败:", error);
    // 错误情况下返回包含success: false的对象
    return {
      success: false,
      message: error instanceof Error ? error.message : '未知错误',
      errors: error instanceof Error ? { general: [error.message] } : undefined
    };
  }
};