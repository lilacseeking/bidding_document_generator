<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>文档总数</span>
            </div>
          </template>
          <div class="card-content">
            <el-statistic :value="statistics.documents">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  文档
                  <el-icon style="margin-left: 4px">
                    <Document />
                  </el-icon>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>模板总数</span>
            </div>
          </template>
          <div class="card-content">
            <el-statistic :value="statistics.templates">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  模板
                  <el-icon style="margin-left: 4px">
                    <Files />
                  </el-icon>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>知识节点</span>
            </div>
          </template>
          <div class="card-content">
            <el-statistic :value="statistics.knowledgeNodes">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  节点
                  <el-icon style="margin-left: 4px">
                    <Connection />
                  </el-icon>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>用户总数</span>
            </div>
          </template>
          <div class="card-content">
            <el-statistic :value="statistics.users">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  用户
                  <el-icon style="margin-left: 4px">
                    <User />
                  </el-icon>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近文档</span>
            </div>
          </template>
          <el-table :data="recentDocuments" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'completed' ? 'success' : 'warning'">
                  {{ row.status === 'completed' ? '已完成' : '进行中' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统公告</span>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="notice in notices"
              :key="notice.id"
              :timestamp="notice.time"
              :type="notice.type"
            >
              {{ notice.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document, Files, Connection, User } from '@element-plus/icons-vue'

const statistics = ref({
  documents: 128,
  templates: 32,
  knowledgeNodes: 1024,
  users: 16
})

const recentDocuments = ref([
  {
    title: '2024年第一季度项目招标文件',
    created_at: '2024-03-15 10:00:00',
    status: 'completed'
  },
  {
    title: '智慧城市建设项目投标书',
    created_at: '2024-03-14 15:30:00',
    status: 'in_progress'
  },
  {
    title: '企业数字化转型方案',
    created_at: '2024-03-13 09:15:00',
    status: 'completed'
  }
])

const notices = ref([
  {
    id: 1,
    content: '系统升级通知：将于本周六凌晨2点进行系统维护',
    time: '2024-03-15 09:00:00',
    type: 'warning'
  },
  {
    id: 2,
    content: '新增知识图谱可视化功能',
    time: '2024-03-14 14:30:00',
    type: 'success'
  },
  {
    id: 3,
    content: '优化文档生成性能，提升处理速度',
    time: '2024-03-13 11:20:00',
    type: 'info'
  }
])
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.stat-card {
  height: 180px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}
</style> 