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
  return await http.get(`${API_BASE}/${projectId}/documents`, { params: filter })
}

// 创建项目文档 - 使用ProjectDocumentIn方式
// 创建项目文档 - 修正URL路径和请求配置
export const createProjectDocument = async (projectId: number, data: ProjectDocumentIn, file: File) => {
  console.log('createProjectDocument - Input data:', projectId, data);
  console.log('File received:', file);
  
  // 创建FormData对象
  const formData = new FormData();
  formData.append('name', data.name);
  formData.append('file', file);
  if (data.remark) {
    formData.append('remark', data.remark);
  }
  
  // 检查FormData内容
  console.log('FormData内容检查:');
  for (const [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
  }
  
  // 修正变量名，使用与函数参数相同的 projectId
  const url = `${API_BASE}/documents/${projectId}/documents`;
  console.log('Sending POST request to:', url);
  
  // 正确的HTTP post调用
  return await http.post(url, formData);
};

// 更新项目文档 - 修正API路径和数据发送方式
export const updateProjectDocument = async (documentId: number, data: ProjectDocumentIn) => {
  // 创建FormData对象
  const formData = new FormData();
  formData.append('name', data.name);
  // formData.append('file', data.file);
  if (data.remark) {
    formData.append('remark', data.remark);
  }
  
  return await http.put(`${API_BASE}/documents/${documentId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

// 删除项目文档 - 修正API路径
export const deleteProjectDocument = async (documentId: number) => {
  return await http.delete(`${API_BASE}/documents/${documentId}`);
}
