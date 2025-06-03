import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || '',
    permissions: []
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
    hasPermission: (state) => (permission) => state.permissions.includes(permission)
  },
  
  actions: {
    setUser(user) {
      this.user = user
    },
    
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    setPermissions(permissions) {
      this.permissions = permissions
    },
    
    login({ token, user }) {
      this.setToken(token)
      this.setUser(user)
    },
    
    logout() {
      this.user = null
      this.token = ''
      this.permissions = []
      localStorage.removeItem('token')
    }
  }
}) 