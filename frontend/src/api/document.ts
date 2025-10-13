// 项目文档相关API
// 导入需要的模块
import { http } from '@/utils/http'

export interface ProjectDocumentIn {
  name: string
  remark?: string | null
}

export interface ProjectDocumentOut {
  id: number
  name: string
  file: string // 添加文件路径字段
  remark?: string | null
}

export interface ProjectDocumentFilter {
  name?: string
  remark?: string | null
}


const API_BASE = '/api/v1/projects'

// 获取项目文档列表
export const getProjectDocuments = async (projectId: number, filter: ProjectDocumentFilter) => {
  // console.log('getProjectDocuments', projectId, filter);
  // 注意：后端API路径为/documents/{project_id}/documents
  // API_BASE已经包含了/api/v1/projects前缀
  const resp = await http.get(`${API_BASE}/documents/${projectId}/documents`, { params: filter })
  // 检查响应数据
  // console.log('getProjectDocuments response:', resp);
  return resp
}

/**
 * 创建项目文档
 * @param projectId 项目ID
 * @param data 文档基本信息
 * @param file 文档文件
 * @returns 创建的文档数据
 */
export const createProjectDocument = async (projectId: number, data: ProjectDocumentIn, file: File) => {
  
  // 创建FormData对象 - 注意：先添加data字段，再添加file字段，与后端参数定义顺序匹配
  const formData = new FormData();
  formData.append('name', data.name);
  if (data.remark) {
    formData.append('remark', data.remark);
  }
  formData.append('file', file);

  // 修正URL路径 - 后端API路径为/projects/documents/{project_id}/documents
  const url = `${API_BASE}/documents/${projectId}/documents`;
   
  // 使用正确的HTTP post调用，按照post方法签名传递参数
  // 第二个参数是配置对象，包含data和headers
  return await http.post(url, {
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

/**
 * 更新项目文档
 * @param documentId 文档ID
 * @param data 文档更新信息
 * @returns 更新后的文档数据
 */
export const updateProjectDocument = async (documentId: number, data: ProjectDocumentIn) => {
  // 创建FormData对象
  const formData = new FormData();
  formData.append('name', data.name);
  // formData.append('file', data.file);
  if (data.remark) {
    formData.append('remark', data.remark);
  }
  
  // 修正API路径
  return await http.put(`${API_BASE}/documents/${documentId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 删除项目文档
 * @param documentId 文档ID
 * @returns 删除结果
 */
export const deleteProjectDocument = async (documentId: number) => {
  // 修正API路径
  // return await http.delete(`${API_BASE}/documents/${documentId}`);
  return await http.post(`${API_BASE}/documents/${documentId}/delete`, {}, { method: 'DELETE' });
  
}

// 下载项目文档文件
export const downloadProjectDocument = async (filePath: string) => {
  // 这是一个辅助函数，实际的下载逻辑在上面的downloadFile中
  let fullUrl = filePath;
  
  // 检查并补全URL
  if (!fullUrl.startsWith('http')) {
    if (!fullUrl.startsWith('/')) {
      fullUrl = '/' + fullUrl;
    }
    fullUrl = window.location.origin + fullUrl;
  }
  
  return {
    url: fullUrl,
    filename: filePath.split('/').pop() || 'document'
  };
};
