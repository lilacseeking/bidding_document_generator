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
            <el-statistic :value="statistics.nodes">
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
    
    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近文档</span>
            </div>
          </template>
          <el-table :data="recentDocuments" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近模板</span>
            </div>
          </template>
          <el-table :data="recentTemplates" style="width: 100%">
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="updated_at" label="更新时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Files, Connection, User } from '@element-plus/icons-vue'

const statistics = ref({
  documents: 0,
  templates: 0,
  nodes: 0,
  users: 0
})

const recentDocuments = ref([])
const recentTemplates = ref([])

onMounted(async () => {
  // TODO: 从API获取统计数据
  statistics.value = {
    documents: 100,
    templates: 50,
    nodes: 200,
    users: 10
  }
  
  // TODO: 从API获取最近文档
  recentDocuments.value = [
    {
      title: '示例文档1',
      type: '投标文件',
      created_at: '2024-01-01 12:00:00'
    },
    {
      title: '示例文档2',
      type: '技术方案',
      created_at: '2024-01-02 12:00:00'
    }
  ]
  
  // TODO: 从API获取最近模板
  recentTemplates.value = [
    {
      name: '示例模板1',
      type: '投标文件',
      updated_at: '2024-01-01 12:00:00'
    },
    {
      name: '示例模板2',
      type: '技术方案',
      updated_at: '2024-01-02 12:00:00'
    }
  ]
})
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.stat-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.mt-4 {
  margin-top: 20px;
}
</style> 