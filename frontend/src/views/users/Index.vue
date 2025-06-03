<template>
  <div class="users-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用户..."
              class="search-input"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select
              v-model="selectedRole"
              placeholder="角色"
              clearable
              @change="handleRoleChange"
            >
              <el-option
                v-for="role in roles"
                :key="role.value"
                :label="role.label"
                :value="role.value"
              />
            </el-select>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="handleCreate">
              <el-icon><Plus /></el-icon>
              新建用户
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="users"
        style="width: 100%"
      >
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="name" label="姓名" min-width="120" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
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
                @click="handleResetPassword(row)"
              >
                重置密码
              </el-button>
              <el-button
                :type="row.status === 'active' ? 'danger' : 'success'"
                link
                @click="handleToggleStatus(row)"
              >
                {{ row.status === 'active' ? '禁用' : '启用' }}
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

    <!-- 创建/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建用户' : '编辑用户'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :disabled="dialogType === 'edit'"
          />
        </el-form-item>
        <el-form-item
          label="密码"
          prop="password"
          v-if="dialogType === 'create'"
        >
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option
              v-for="role in roles"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话" />
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

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPasswordVisible"
      title="重置密码"
      width="400px"
    >
      <el-form
        ref="resetPasswordFormRef"
        :model="resetPasswordForm"
        :rules="resetPasswordRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="password">
          <el-input
            v-model="resetPasswordForm.password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="resetPasswordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPasswordVisible = false">取消</el-button>
          <el-button type="primary" @click="handleResetPasswordSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 状态变量
const loading = ref(false)
const users = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const selectedRole = ref('')
const dialogVisible = ref(false)
const dialogType = ref('create')
const resetPasswordVisible = ref(false)

// 角色选项
const roles = [
  { label: '管理员', value: 'admin' },
  { label: '普通用户', value: 'user' },
  { label: '审核员', value: 'reviewer' }
]

// 表单相关
const formRef = ref(null)
const form = ref({
  username: '',
  password: '',
  name: '',
  role: '',
  email: '',
  phone: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 重置密码表单相关
const resetPasswordFormRef = ref(null)
const resetPasswordForm = ref({
  userId: '',
  password: '',
  confirmPassword: ''
})

const resetPasswordRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetPasswordForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 方法
const getRoleType = (role) => {
  const types = {
    admin: 'danger',
    reviewer: 'warning',
    user: 'info'
  }
  return types[role] || 'info'
}

const getRoleLabel = (role) => {
  const roleObj = roles.find(r => r.value === role)
  return roleObj ? roleObj.label : role
}

const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

const handleRoleChange = () => {
  currentPage.value = 1
  fetchUsers()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchUsers()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchUsers()
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.value = {
    username: '',
    password: '',
    name: '',
    role: '',
    email: '',
    phone: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = {
    username: row.username,
    name: row.name,
    role: row.role,
    email: row.email,
    phone: row.phone
  }
  dialogVisible.value = true
}

const handleResetPassword = (row) => {
  resetPasswordForm.value = {
    userId: row.id,
    password: '',
    confirmPassword: ''
  }
  resetPasswordVisible.value = true
}

const handleToggleStatus = (row) => {
  const action = row.status === 'active' ? '禁用' : '启用'
  ElMessageBox.confirm(
    `确定要${action}该用户吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      loading.value = true
      // TODO: 实现用户状态切换
      ElMessage.success(`${action}成功`)
      fetchUsers()
    } catch (error) {
      console.error(`${action}失败:`, error)
      ElMessage.error(`${action}失败`)
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
    
    // TODO: 实现用户创建/更新
    ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

const handleResetPasswordSubmit = async () => {
  if (!resetPasswordFormRef.value) return
  
  try {
    await resetPasswordFormRef.value.validate()
    loading.value = true
    
    // TODO: 实现密码重置
    ElMessage.success('密码重置成功')
    resetPasswordVisible.value = false
  } catch (error) {
    console.error('密码重置失败:', error)
    ElMessage.error('密码重置失败')
  } finally {
    loading.value = false
  }
}

const fetchUsers = async () => {
  try {
    loading.value = true
    // TODO: 实现用户列表获取
    users.value = [
      {
        id: 1,
        username: 'admin',
        name: '管理员',
        role: 'admin',
        email: 'admin@example.com',
        phone: '13800138000',
        status: 'active',
        created_at: '2024-01-01 12:00:00'
      },
      {
        id: 2,
        username: 'user1',
        name: '张三',
        role: 'user',
        email: 'user1@example.com',
        phone: '13800138001',
        status: 'active',
        created_at: '2024-01-02 12:00:00'
      }
    ]
    total.value = 100
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  gap: 16px;
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