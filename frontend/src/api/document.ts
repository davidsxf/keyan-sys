// 项目文档相关API
import { http } from '@/utils/http'


export interface ProjectDocumentIn {
  name: string
  file: File
  remark?: string
}

export interface ProjectDocumentOut {
  id: number
  name: string
  file: File
  remark?: string
}

export interface ProjectDocumentFilter {
  name?: string
  remark?: string
}


const API_BASE = '/api/v1/projects'

// 获取项目文档列表
export const getProjectDocuments = async (projectId: number, filter: ProjectDocumentFilter) => {
  return await http.get(`${API_BASE}/${projectId}/documents`, { params: filter })
}

// 创建项目文档
export const createProjectDocument = async (projectId: number, data: ProjectDocumentIn) => {
  return await http.post(`${API_BASE}/${projectId}/documents`, { data })
}

// 更新项目文档
export const updateProjectDocument = async (projectId: number, documentId: number, data: ProjectDocumentIn) => {
  return await http.post(`${API_BASE}/${projectId}/documents/${documentId}`, { data }, { method: 'PUT' })
}

// 删除项目文档
export const deleteProjectDocument = async (projectId: number, documentId: number) => {
  return await http.post(`${API_BASE}/${projectId}/documents/${documentId}`, {}, { method: 'DELETE' })
}
