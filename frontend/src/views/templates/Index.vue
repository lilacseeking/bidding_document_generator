<template>
  <div class="templates-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索模板..."
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
              新建模板
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="templates"
        style="width: 100%"
      >
        <el-table-column prop="name" label="名称" min-width="200" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="version" label="版本" width="100" />
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

    <!-- 创建/编辑模板对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建模板' : '编辑模板'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择模板类型">
            <el-option label="投标文件" value="投标文件" />
            <el-option label="技术方案" value="技术方案" />
            <el-option label="商务文件" value="商务文件" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本" prop="version">
          <el-input v-model="form.version" placeholder="请输入版本号" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入模板描述"
          />
        </el-form-item>
        <el-form-item label="文件" prop="file">
          <el-upload
            class="upload-demo"
            action="/api/templates/upload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 .docx, .xlsx, .pptx 格式文件
              </div>
            </template>
          </el-upload>
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
      title="模板预览"
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
  name: '',
  type: '',
  version: '',
  description: '',
  file: null
})

const rules = {
  name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择模板类型', trigger: 'change' }
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' }
  ]
}

// 方法
const handleSearch = () => {
  currentPage.value = 1
  fetchTemplates()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchTemplates()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTemplates()
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.value = {
    name: '',
    type: '',
    version: '',
    description: '',
    file: null
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handlePreview = (row) => {
  previewUrl.value = `/api/templates/${row.id}/preview`
  previewVisible.value = true
}

const handleExport = async (row) => {
  try {
    loading.value = true
    // TODO: 实现模板导出
    ElMessage.success('模板导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('模板导出失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该模板吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      loading.value = true
      // TODO: 实现模板删除
      ElMessage.success('删除成功')
      fetchTemplates()
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
    
    // TODO: 实现模板创建/更新
    ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
    dialogVisible.value = false
    fetchTemplates()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

const beforeUpload = (file) => {
  const isValidType = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation'
  ].includes(file.type)
  
  if (!isValidType) {
    ElMessage.error('只能上传 Word、Excel 或 PowerPoint 文件！')
    return false
  }
  
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }
  
  return true
}

const handleUploadSuccess = (response) => {
  form.value.file = response.data
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const fetchTemplates = async () => {
  try {
    loading.value = true
    // TODO: 实现模板列表获取
    templates.value = [
      {
        id: 1,
        name: '示例模板1',
        type: '投标文件',
        version: '1.0.0',
        creator: 'admin',
        created_at: '2024-01-01 12:00:00',
        updated_at: '2024-01-01 12:00:00'
      },
      {
        id: 2,
        name: '示例模板2',
        type: '技术方案',
        version: '1.0.0',
        creator: 'admin',
        created_at: '2024-01-02 12:00:00',
        updated_at: '2024-01-02 12:00:00'
      }
    ]
    total.value = 100
  } catch (error) {
    console.error('获取模板列表失败:', error)
    ElMessage.error('获取模板列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTemplates()
})
</script>

<style scoped>
.templates-container {
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

.upload-demo {
  width: 100%;
}
</style> 