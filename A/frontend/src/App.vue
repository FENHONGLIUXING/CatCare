<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 1. 定义响应式变量，用来存放从后端拿到的数字
const count = ref(0)

// 2. 获取初始计数的函数
const getInitialCount = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/get_count')
    count.value = response.data.count
  } catch (error) {
    console.error('获取计数失败:', error)
  }
}

// 3. 点击按钮增加计数的函数
const addCount = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/increment')
    // 更新本地显示的数字为后端返回的新数字
    count.value = response.data.new_count
  } catch (error) {
    console.error('增加计数失败:', error)
  }
}

// 4. 生命周期钩子：页面一加载就去后端领数据
onMounted(() => {
  getInitialCount()
})
</script>

<template>
  <div class="container">
    <h1>校园猫咪社区计数器</h1>
    
    <p>当前全校累计点击：<strong>{{ count }}</strong> 次</p>
    
    <button @click="addCount">点我加 1</button>
  </div>
</template>

<style scoped></style>
