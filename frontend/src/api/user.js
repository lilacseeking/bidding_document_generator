import request from './request'

export function getInfo() {
  return request({
    url: '/api/v1/users/me',
    method: 'get'
  })
}

export function getUsers(params) {
  return request({
    url: '/api/v1/users',
    method: 'get',
    params
  })
}

export function createUser(data) {
  return request({
    url: '/api/v1/users',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: `/api/v1/users/${id}`,
    method: 'put',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: `/api/v1/users/${id}`,
    method: 'delete'
  })
} 