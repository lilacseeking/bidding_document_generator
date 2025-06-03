<template>
  <div class="documents-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文档..."
              class="search-input"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="handleCreate">
              <el-icon><Plus /></el-icon>
              新建文档
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="documents"
        style="width: 100%"
      >
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                type="primary"
                link
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button
                type="primary"
                link
                @click="handlePreview(row)"
              >
                预览
              </el-button>
              <el-button
                type="primary"
                link
                @click="handleExport(row)"
              >
                导出
              </el-button>
              <el-button
                type="danger"
                link
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 创建/编辑文档对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建文档' : '编辑文档'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择文档类型">
            <el-option label="投标文件" value="投标文件" />
            <el-option label="技术方案" value="技术方案" />
            <el-option label="商务文件" value="商务文件" />
          </el-select>
        </el-form-item>
        <el-form-item label="模板" prop="template_id">
          <el-select v-model="form.template_id" placeholder="请选择模板">
            <el-option
              v-for="template in templates"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入文档描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="文档预览"
      width="80%"
      fullscreen
    >
      <iframe
        v-if="previewUrl"
        :src="previewUrl"
        style="width: 100%; height: 80vh; border: none;"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 状态变量
const loading = ref(false)
const documents = ref([])
const templates = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const dialogVisible = ref(false)
const dialogType = ref('create')
const previewVisible = ref(false)
const previewUrl = ref('')

// 表单相关
const formRef = ref(null)
const form = ref({
  title: '',
  type: '',
  template_id: '',
  description: ''
})

const rules = {
  title: [
    { required: true, message: '请输入文档标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择文档类型', trigger: 'change' }
  ],
  template_id: [
    { required: true, message: '请选择模板', trigger: 'change' }
  ]
}

// 方法
const getStatusType = (status) => {
  const types = {
    '草稿': 'info',
    '审核中': 'warning',
    '已发布': 'success',
    '已拒绝': 'danger'
  }
  return types[status] || 'info'
}

const handleSearch = () => {
  currentPage.value = 1
  fetchDocuments()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchDocuments()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchDocuments()
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.value = {
    title: '',
    type: '',
    template_id: '',
    description: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handlePreview = (row) => {
  previewUrl.value = `/api/documents/${row.id}/preview`
  previewVisible.value = true
}

const handleExport = async (row) => {
  try {
    loading.value = true
    // TODO: 实现文档导出
    ElMessage.success('文档导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('文档导出失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该文档吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      loading.value = true
      // TODO: 实现文档删除
      ElMessage.success('删除成功')
      fetchDocuments()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    } finally {
      loading.value = false
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // TODO: 实现文档创建/更新
    ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
    dialogVisible.value = false
    fetchDocuments()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

const fetchDocuments = async () => {
  try {
    loading.value = true
    // TODO: 实现文档列表获取
    documents.value = [
      {
        id: 1,
        title: '示例文档1',
        type: '投标文件',
        status: '草稿',
        creator: 'admin',
        created_at: '2024-01-01 12:00:00',
        updated_at: '2024-01-01 12:00:00'
      },
      {
        id: 2,
        title: '示例文档2',
        type: '技术方案',
        status: '已发布',
        creator: 'admin',
        created_at: '2024-01-02 12:00:00',
        updated_at: '2024-01-02 12:00:00'
      }
    ]
    total.value = 100
  } catch (error) {
    console.error('获取文档列表失败:', error)
    ElMessage.error('获取文档列表失败')
  } finally {
    loading.value = false
  }
}

const fetchTemplates = async () => {
  try {
    // TODO: 实现模板列表获取
    templates.value = [
      {
        id: 1,
        name: '示例模板1',
        type: '投标文件'
      },
      {
        id: 2,
        name: '示例模板2',
        type: '技术方案'
      }
    ]
  } catch (error) {
    console.error('获取模板列表失败:', error)
    ElMessage.error('获取模板列表失败')
  }
}

onMounted(() => {
  fetchDocuments()
  fetchTemplates()
})
</script>

<style scoped>
.documents-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 