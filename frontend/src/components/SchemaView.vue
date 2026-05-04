<template>
  <div style="margin-bottom: 20px">
    <el-button @click="loadSchema">查看数据库结构</el-button>

    <el-collapse v-if="schemaData">
      <el-collapse-item
        v-for="(cols, table) in schemaData"
        :key="table"
        :title="table"
      >
        <el-table :data="cols" size="small">
          <el-table-column prop="Field" label="字段名" />
          <el-table-column prop="Type" label="类型" />
          <el-table-column prop="Null" label="是否为空" />
          <el-table-column prop="Key" label="键" />
        </el-table>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../api/request'

const schemaData = ref(null)

const loadSchema = async () => {
  const res = await request.get('/schema/')
  schemaData.value = res.data
}
</script>