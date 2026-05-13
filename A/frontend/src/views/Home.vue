<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const catsWithRecords = ref([])

const getCatsWithRecords = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/cats-with-records')
    catsWithRecords.value = response.data.filter(cat => cat.feedings && cat.feedings.length > 0)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${month}/${day} ${hours}:${minutes}`
}

onMounted(() => {
  getCatsWithRecords()
})
</script>

<template>
  <div class="home">
    <header class="header">
      <h1>CatCare</h1>
      <p>校园猫咪社区</p>
    </header>

    <nav class="nav-cards">
      <router-link to="/cats" class="card">
        <span>猫咪档案</span>
      </router-link>
      <router-link to="/feeding" class="card">
        <span>投喂记录</span>
      </router-link>
    </nav>

    <section class="latest">
      <h2>最新动态</h2>
      <div class="cards-grid">
        <div v-if="catsWithRecords.length === 0" class="empty">
          暂无喂养记录
        </div>
        <div v-for="cat in catsWithRecords" :key="cat.id" class="cat-card">
          <div class="card-header">
            <div class="cat-avatar" v-if="cat.image_url">
              <img :src="'http://127.0.0.1:5000' + cat.image_url" :alt="cat.name" />
            </div>
            <div class="cat-avatar placeholder" v-else>
              <span>?</span>
            </div>
            <h3>{{ cat.name }}</h3>
          </div>
          <div class="card-body">
            <div v-for="feeding in cat.feedings" :key="feeding.id" class="feeding-item">
              <span class="feeding-time">{{ formatTime(feeding.time) }}</span>
              <span class="feeding-food">{{ feeding.food_type }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 80px 20px;
}

.header {
  text-align: center;
  margin-bottom: 80px;
  padding-bottom: 30px;
  border-bottom: 1px solid #000000;
}

.header h1 {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 42px;
  font-weight: 300;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.header p {
  font-size: 14px;
  letter-spacing: 0.1em;
  color: #666666;
}

.nav-cards {
  display: flex;
  gap: 16px;
  margin-bottom: 80px;
}

.card {
  flex: 1;
  padding: 28px 20px;
  border: 1px solid #000000;
  text-decoration: none;
  color: #ffffff;
  background: #000000;
  text-align: center;
  transition: all 0.3s;
  font-size: 16px;
  letter-spacing: 0.05em;
}

.card:hover {
  background: #ffffff;
  color: #000000;
}

.latest {
  border-top: 1px solid #000000;
  padding-top: 30px;
}

.latest h2 {
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.cat-card {
  border: 1px solid #000000;
  transition: all 0.2s;
}

.cat-card:hover {
  transform: translateY(-4px);
  box-shadow: 4px 4px 0px #000000;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #eeeeee;
}

.cat-avatar {
  width: 48px;
  height: 48px;
  border: 1px solid #000000;
  overflow: hidden;
  flex-shrink: 0;
}

.cat-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cat-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999999;
  font-size: 20px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.card-body {
  padding: 12px 16px;
  min-height: 108px;
}

.feeding-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #eeeeee;
}

.feeding-item:last-child {
  border-bottom: none;
}

.feeding-time {
  font-size: 12px;
  color: #999999;
}

.feeding-food {
  font-size: 13px;
  color: #000000;
}

.empty {
  grid-column: 1 / -1;
  padding: 60px;
  text-align: center;
  color: #999999;
  font-size: 14px;
  border: 1px dashed #dddddd;
}
</style>