// 项目文档相关API
// 导入需要的模块
import { http } from '@/utils/http'

export interface ProjectDocumentIn {
  name: string
  file: File
  remark?: string | null
}

export interface ProjectDocumentOut {
  id: number
  name: string
  file: File
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

// 创建项目文档 - 修改数据发送方式，使用FormData处理文件上传
export const createProjectDocument = async (projectId: number, data: ProjectDocumentIn | FormData) => {
  console.log('createProjectDocument - Input data:', projectId, data);
  
  let formData: FormData;
  
  // 判断传入的数据是FormData还是ProjectDocumentIn对象
  if (data instanceof FormData) {
    // 如果是FormData对象，直接使用，但需要添加project_id
    formData = data;
    formData.append('project_id', projectId.toString());
  } else {
    // 如果是ProjectDocumentIn对象，创建新的FormData
    formData = new FormData();
    formData.append('project_id', projectId.toString());
    formData.append('name', data.name);
    formData.append('file', data.file);
    if (data.remark) {
      formData.append('remark', data.remark);
    }
  }
  
  // 正确检查FormData内容的方法
  console.log('FormData内容检查:');
  for (const [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
  }
  
  // 修改请求URL，移除project_id参数，因为它已经在FormData中
  return await http.post(`${API_BASE}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

// 更新项目文档 - 修正API路径和数据发送方式
export const updateProjectDocument = async (documentId: number, data: ProjectDocumentIn) => {
  // 创建FormData对象
  const formData = new FormData();
  formData.append('name', data.name);
  formData.append('file', data.file);
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
