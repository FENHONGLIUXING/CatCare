<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const count = ref(0)

const getInitialCount = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/get_count')
    count.value = response.data.count
  } catch (error) {
    console.error('获取计数失败:', error)
  }
}

const addCount = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/increment')
    count.value = response.data.new_count
  } catch (error) {
    console.error('增加计数失败:', error)
  }
}

onMounted(() => {
  getInitialCount()
})
</script>

<template>
  <div class="home">
    <header class="header">
      <h1>CatCare</h1>
      <p>校园猫咪社区</p>
    </header>

    <div class="counter-box">
      <p class="label">全校累计点击</p>
      <p class="count">{{ count }}</p>
      <button @click="addCount">点我加 1</button>
    </div>

    <nav class="nav-cards">
      <router-link to="/cats" class="card">
        <h2>猫咪档案</h2>
        <p>查看和管理猫咪信息</p>
      </router-link>
      <router-link to="/feeding" class="card">
        <h2>投喂记录</h2>
        <p>记录猫咪投喂情况</p>
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
.home {
  max-width: 600px;
  margin: 0 auto;
  padding: 60px 20px;
}

.header {
  text-align: center;
  margin-bottom: 60px;
  border-bottom: 2px solid #000000;
  padding-bottom: 30px;
}

.header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.header p {
  font-size: 14px;
  color: #666666;
}

.counter-box {
  text-align: center;
  margin-bottom: 60px;
  padding: 40px;
  border: 2px solid #000000;
}

.counter-box .label {
  font-size: 14px;
  margin-bottom: 10px;
}

.counter-box .count {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 30px;
}

.counter-box button {
  background: #000000;
  color: #ffffff;
  border: none;
  padding: 14px 40px;
  font-size: 14px;
  cursor: pointer;
}

.counter-box button:hover {
  background: #333333;
}

.nav-cards {
  display: flex;
  gap: 20px;
}

.card {
  flex: 1;
  padding: 40px 30px;
  border: 2px solid #000000;
  text-decoration: none;
  color: #000000;
  text-align: center;
  transition: all 0.2s;
}

.card:hover {
  background: #000000;
  color: #ffffff;
}

.card:hover h2,
.card:hover p {
  color: #ffffff;
}

.card h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
}

.card p {
  font-size: 13px;
  color: #666666;
}
</style>