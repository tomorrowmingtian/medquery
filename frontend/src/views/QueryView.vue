<template>
  <div style="max-width: 900px">

    <!-- 标题 -->
    <h3>自然语言查询</h3>

    <!-- 输入区 -->
    <div style="display: flex; gap: 10px; margin-bottom: 20px">
      <el-input
        v-model="text"
        placeholder="例如：查询糖尿病患者数量"
        clearable
        @keyup.enter="handleQuery"
      />
      <el-button type="primary" @click="handleQuery" :loading="loading">
        查询
      </el-button>
    </div>

    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      style="margin-bottom: 15px"
    />

    <!-- SQL展示 -->
    <el-card v-if="sql" shadow="never" style="margin-bottom: 20px">
      <template #header>
        <b>生成SQL</b>
      </template>
      <pre style="margin: 0; color: #409eff">{{ sql }}</pre>
    </el-card>

    <!-- 表格 -->
    <el-table
      v-if="tableData.length"
      :data="tableData"
      border
      stripe
      style="width: 100%"
    >
      <el-table-column
        v-for="(value, key) in tableData[0]"
        :key="key"
        :prop="key"
        :label="key"
      />
    </el-table>

    <!-- 空状态 -->
    <el-empty v-else-if="sql && !loading" description="暂无数据" />

    <!-- 查询历史 -->
    <div v-if="history.length" style="margin-top: 40px">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <h4>查询历史</h4>
        <el-button size="small" @click="handleClearHistory">清空历史</el-button>
      </div>
      <el-collapse>
        <el-collapse-item
          v-for="(item, index) in history"
          :key="index"
          :title="formatTime(item.time) + '  ' + item.text"
        >
          <pre style="color: #409eff; margin: 0 0 10px">{{ item.sql }}</pre>
          <el-button size="small" @click="text = item.text">回填查询</el-button>
        </el-collapse-item>
      </el-collapse>
    </div>

  </div>
  <SchemaView />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../api/request'
import SchemaView from '../components/SchemaView.vue'
import { loadHistory, saveHistory, clearHistory } from '../utils/history'

const text = ref('')
const sql = ref('')
const tableData = ref([])
const loading = ref(false)
const error = ref('')
const history = ref([])

onMounted(() => {
  history.value = loadHistory()
})

const formatTime = (ts) => {
  const d = new Date(ts)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
}

const handleClearHistory = () => {
  clearHistory()
  history.value = []
}

const handleQuery = async () => {
  if (!text.value) return

  loading.value = true
  error.value = ''
  sql.value = ''
  tableData.value = []

  try {
    const res = await request.post('/query/', {
      text: text.value
    })

    sql.value = res.sql

    if (res.success) {
      tableData.value = res.data || []
      saveHistory({ text: text.value, sql: res.sql })
      history.value = loadHistory()
    } else {
      error.value = res.error || '查询失败'
    }

  } catch (e) {
    error.value = '请求失败，请检查后端服务'
  } finally {
    loading.value = false
  }
}
</script>