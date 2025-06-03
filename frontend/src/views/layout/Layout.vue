<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :default-active="route.path"
        class="el-menu-vertical"
        :router="true"
        :collapse="isCollapse"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/documents">
          <el-icon><Document /></el-icon>
          <span>文档管理</span>
        </el-menu-item>
        <el-menu-item index="/templates">
          <el-icon><Files /></el-icon>
          <span>模板管理</span>
        </el-menu-item>
        <el-menu-item index="/knowledge">
          <el-icon><Connection /></el-icon>
          <span>知识图谱</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header height="60px">
        <div class="header-left">
          <el-button
            type="text"
            @click="toggleCollapse"
          >
            <el-icon>
              <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </el-icon>
          </el-button>
          <h2>{{ route.meta.title || '投标文档生成系统' }}</h2>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-dropdown">
              {{ userStore.currentUser?.username || '用户' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  HomeFilled,
  Document,
  Files,
  Connection,
  User,
  Expand,
  Fold,
  ArrowDown
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-menu-vertical {
  height: 100%;
  border-right: none;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.el-main {
  background-color: var(--background-color);
  padding: 20px;
}
</style> 