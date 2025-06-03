<template>
  <div class="knowledge-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索节点..."
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
              v-model="selectedType"
              placeholder="节点类型"
              clearable
              @change="handleTypeChange"
            >
              <el-option
                v-for="type in nodeTypes"
                :key="type"
                :label="type"
                :value="type"
              />
            </el-select>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="handleCreate">
              <el-icon><Plus /></el-icon>
              新建节点
            </el-button>
          </div>
        </div>
      </template>

      <div class="graph-container" ref="graphContainer"></div>
    </el-card>

    <!-- 创建/编辑节点对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建节点' : '编辑节点'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入节点名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择节点类型">
            <el-option
              v-for="type in nodeTypes"
              :key="type"
              :label="type"
              :value="type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入节点描述"
          />
        </el-form-item>
        <el-form-item label="属性" prop="properties">
          <div
            v-for="(value, key) in form.properties"
            :key="key"
            class="property-item"
          >
            <el-input
              v-model="form.properties[key]"
              :placeholder="`请输入${key}`"
            >
              <template #prepend>{{ key }}</template>
              <template #append>
                <el-button
                  type="danger"
                  link
                  @click="removeProperty(key)"
                >
                  删除
                </el-button>
              </template>
            </el-input>
          </div>
          <div class="property-add">
            <el-input
              v-model="newPropertyKey"
              placeholder="属性名"
              style="width: 200px"
            />
            <el-button
              type="primary"
              @click="addProperty"
              :disabled="!newPropertyKey"
            >
              添加属性
            </el-button>
          </div>
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

    <!-- 创建关系对话框 -->
    <el-dialog
      v-model="relationDialogVisible"
      title="创建关系"
      width="600px"
    >
      <el-form
        ref="relationFormRef"
        :model="relationForm"
        :rules="relationRules"
        label-width="100px"
      >
        <el-form-item label="源节点" prop="source">
          <el-select
            v-model="relationForm.source"
            placeholder="请选择源节点"
            filterable
          >
            <el-option
              v-for="node in nodes"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关系类型" prop="type">
          <el-select
            v-model="relationForm.type"
            placeholder="请选择关系类型"
          >
            <el-option
              v-for="type in relationTypes"
              :key="type"
              :label="type"
              :value="type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="目标节点" prop="target">
          <el-select
            v-model="relationForm.target"
            placeholder="请选择目标节点"
            filterable
          >
            <el-option
              v-for="node in nodes"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="属性" prop="properties">
          <div
            v-for="(value, key) in relationForm.properties"
            :key="key"
            class="property-item"
          >
            <el-input
              v-model="relationForm.properties[key]"
              :placeholder="`请输入${key}`"
            >
              <template #prepend>{{ key }}</template>
              <template #append>
                <el-button
                  type="danger"
                  link
                  @click="removeRelationProperty(key)"
                >
                  删除
                </el-button>
              </template>
            </el-input>
          </div>
          <div class="property-add">
            <el-input
              v-model="newRelationPropertyKey"
              placeholder="属性名"
              style="width: 200px"
            />
            <el-button
              type="primary"
              @click="addRelationProperty"
              :disabled="!newRelationPropertyKey"
            >
              添加属性
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="relationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRelationSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as d3 from 'd3'
import { forceSimulation, forceLink, forceManyBody, forceCenter } from 'd3-force'

// 状态变量
const loading = ref(false)
const searchQuery = ref('')
const selectedType = ref('')
const nodeTypes = ref(['项目', '技术', '设备', '人员', '文档'])
const relationTypes = ref(['包含', '使用', '负责', '参考'])
const nodes = ref([])
const graphContainer = ref(null)
const simulation = ref(null)
const svg = ref(null)
const dialogVisible = ref(false)
const dialogType = ref('create')
const relationDialogVisible = ref(false)

// 表单相关
const formRef = ref(null)
const form = ref({
  name: '',
  type: '',
  description: '',
  properties: {}
})

const rules = {
  name: [
    { required: true, message: '请输入节点名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择节点类型', trigger: 'change' }
  ]
}

// 关系表单相关
const relationFormRef = ref(null)
const relationForm = ref({
  source: '',
  type: '',
  target: '',
  properties: {}
})

const relationRules = {
  source: [
    { required: true, message: '请选择源节点', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择关系类型', trigger: 'change' }
  ],
  target: [
    { required: true, message: '请选择目标节点', trigger: 'change' }
  ]
}

// 属性相关
const newPropertyKey = ref('')
const newRelationPropertyKey = ref('')

// 方法
const handleSearch = () => {
  fetchGraphData()
}

const handleTypeChange = () => {
  fetchGraphData()
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.value = {
    name: '',
    type: '',
    description: '',
    properties: {}
  }
  dialogVisible.value = true
}

const handleEdit = (node) => {
  dialogType.value = 'edit'
  form.value = { ...node }
  dialogVisible.value = true
}

const handleDelete = (node) => {
  ElMessageBox.confirm(
    '确定要删除该节点吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      loading.value = true
      // TODO: 实现节点删除
      ElMessage.success('删除成功')
      fetchGraphData()
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
    
    // TODO: 实现节点创建/更新
    ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
    dialogVisible.value = false
    fetchGraphData()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

const addProperty = () => {
  if (newPropertyKey.value) {
    form.value.properties[newPropertyKey.value] = ''
    newPropertyKey.value = ''
  }
}

const removeProperty = (key) => {
  delete form.value.properties[key]
}

const addRelationProperty = () => {
  if (newRelationPropertyKey.value) {
    relationForm.value.properties[newRelationPropertyKey.value] = ''
    newRelationPropertyKey.value = ''
  }
}

const removeRelationProperty = (key) => {
  delete relationForm.value.properties[key]
}

const handleRelationSubmit = async () => {
  if (!relationFormRef.value) return
  
  try {
    await relationFormRef.value.validate()
    loading.value = true
    
    // TODO: 实现关系创建
    ElMessage.success('创建成功')
    relationDialogVisible.value = false
    fetchGraphData()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

const fetchGraphData = async () => {
  try {
    loading.value = true
    // TODO: 实现图谱数据获取
    const data = {
      nodes: [
        {
          id: '1',
          name: '示例节点1',
          type: '项目',
          description: '这是一个示例节点'
        },
        {
          id: '2',
          name: '示例节点2',
          type: '技术',
          description: '这是另一个示例节点'
        }
      ],
      links: [
        {
          source: '1',
          target: '2',
          type: '使用'
        }
      ]
    }
    
    nodes.value = data.nodes
    updateGraph(data)
  } catch (error) {
    console.error('获取图谱数据失败:', error)
    ElMessage.error('获取图谱数据失败')
  } finally {
    loading.value = false
  }
}

const updateGraph = (data) => {
  if (!graphContainer.value) return

  // 清除现有内容
  d3.select(graphContainer.value).selectAll('*').remove()

  // 创建 SVG
  svg.value = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')

  // 创建连线
  const link = svg.value.append('g')
    .selectAll('line')
    .data(data.links)
    .enter()
    .append('line')
    .attr('stroke', '#999')
    .attr('stroke-opacity', 0.6)
    .attr('stroke-width', 1)

  // 创建节点
  const node = svg.value.append('g')
    .selectAll('circle')
    .data(data.nodes)
    .enter()
    .append('circle')
    .attr('r', 5)
    .attr('fill', d => {
      const colors = {
        '项目': '#409EFF',
        '技术': '#67C23A',
        '设备': '#E6A23C',
        '人员': '#F56C6C',
        '文档': '#909399'
      }
      return colors[d.type] || '#909399'
    })
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  // 添加节点标签
  const label = svg.value.append('g')
    .selectAll('text')
    .data(data.nodes)
    .enter()
    .append('text')
    .text(d => d.name)
    .attr('font-size', 12)
    .attr('dx', 12)
    .attr('dy', 4)

  // 创建力导向图
  simulation.value = forceSimulation(data.nodes)
    .force('link', forceLink(data.links).id(d => d.id).distance(100))
    .force('charge', forceManyBody().strength(-300))
    .force('center', forceCenter(
      graphContainer.value.clientWidth / 2,
      graphContainer.value.clientHeight / 2
    ))

  // 更新位置
  simulation.value.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)

    label
      .attr('x', d => d.x)
      .attr('y', d => d.y)
  })

  // 添加点击事件
  node.on('click', (event, d) => {
    handleEdit(d)
  })
}

// 拖拽相关函数
function dragstarted(event, d) {
  if (!event.active) simulation.value.alphaTarget(0.3).restart()
  d.fx = d.x
  d.fy = d.y
}

function dragged(event, d) {
  d.fx = event.x
  d.fy = event.y
}

function dragended(event, d) {
  if (!event.active) simulation.value.alphaTarget(0)
  d.fx = null
  d.fy = null
}

onMounted(() => {
  fetchGraphData()
})

onUnmounted(() => {
  if (simulation.value) {
    simulation.value.stop()
  }
})
</script>

<style scoped>
.knowledge-container {
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

.graph-container {
  height: calc(100vh - 200px);
  background-color: #f5f7fa;
  border-radius: 4px;
}

.property-item {
  margin-bottom: 16px;
}

.property-add {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
</style> 