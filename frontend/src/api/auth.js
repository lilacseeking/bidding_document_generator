import request from './request'

export function login(data) {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

export function testToken() {
  return request({
    url: '/api/v1/auth/test-token',
    method: 'post'
  })
} 