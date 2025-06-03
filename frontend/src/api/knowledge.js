import request from '@/utils/request'

export function getKnowledgeGraph() {
  return request({
    url: '/api/v1/knowledge/graph',
    method: 'get'
  })
}

export function getNode(id) {
  return request({
    url: `/api/v1/knowledge/nodes/${id}`,
    method: 'get'
  })
}

export function addNode(data) {
  return request({
    url: '/api/v1/knowledge/nodes',
    method: 'post',
    data
  })
}

export function updateNode(id, data) {
  return request({
    url: `/api/v1/knowledge/nodes/${id}`,
    method: 'put',
    data
  })
}

export function deleteNode(id) {
  return request({
    url: `/api/v1/knowledge/nodes/${id}`,
    method: 'delete'
  })
}

export function addRelationship(data) {
  return request({
    url: '/api/v1/knowledge/relationships',
    method: 'post',
    data
  })
}

export function deleteRelationship(id) {
  return request({
    url: `/api/v1/knowledge/relationships/${id}`,
    method: 'delete'
  })
}

export function searchNodes(query) {
  return request({
    url: '/api/v1/knowledge/search',
    method: 'get',
    params: { query }
  })
}

export function getNodeTypes() {
  return request({
    url: '/api/v1/knowledge/types',
    method: 'get'
  })
}

export function getRelationshipTypes() {
  return request({
    url: '/api/v1/knowledge/relationship-types',
    method: 'get'
  })
} 