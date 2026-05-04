<template>
  <div class="container">
    <div class="content">
      <h2 style="text-align: center; margin-bottom: 30px;">
        医疗 NLP2SQL 查询系统
      </h2>

      <QueryView />
    </div>
  </div>
</template>

<script setup>
import QueryView from './views/QueryView.vue'
</script>

<style>
/* 整个页面居中 */
.container {
  display: flex;
  justify-content: center;   /* 水平居中 */
  align-items: flex-start;   /* 顶部对齐（更自然） */
  min-height: 100vh;
  background: #f5f7fa;
}

/* 内容区域 */
.content {
  width: 900px;
  margin-top: 60px;
}
</style>