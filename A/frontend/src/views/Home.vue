<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据：存储猫咪及其今日喂养记录
const catsWithRecords = ref([])

// 获取猫咪及其今日最近3条喂养记录
const getCatsWithRecords = async () => {
  try {
    // 调用后端API获取数据
    const response = await request.get('/api/cats-with-records')
    // 过滤掉没有喂养记录的猫咪
    catsWithRecords.value = response.data.filter(cat => cat.feedings && cat.feedings.length > 0)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

// 格式化时间字符串（转换为 MM/DD HH:MM 格式）
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${month}/${day} ${hours}:${minutes}`
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  getCatsWithRecords()
})
</script>

<template>
  <!-- 首页主容器 -->
  <div class="home">
    <div class="user-bar">
      <span class="user-info">👤 {{ authStore.username }}</span>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </div>

    <header class="header">
      <h1>CatCare</h1>
      <p>校园猫咪社区</p>
    </header>

    <!-- 导航卡片：通往猫咪档案和投喂记录页面 -->
    <nav class="nav-cards">
      <router-link to="/cats" class="card">
        <span>猫咪档案</span>
      </router-link>
      <router-link to="/feeding" class="card">
        <span>投喂记录</span>
      </router-link>
    </nav>

    <!-- 最新动态：展示今日有喂养记录的猫咪 -->
    <section class="latest">
      <h2>最新动态</h2>
      <div class="cards-grid">
        <!-- 空状态：没有今日喂养记录时显示 -->
        <div v-if="catsWithRecords.length === 0" class="empty">
          暂无喂养记录
        </div>
        <!-- 猫咪卡片循环渲染 -->
        <div v-for="cat in catsWithRecords" :key="cat.id" class="cat-card">
          <!-- 卡片头部：头像 + 名字 -->
          <div class="card-header">
            <!-- 猫咪头像（有图片时） -->
            <div class="cat-avatar" v-if="cat.image_url">
              <img :src="'http://127.0.0.1:5000' + cat.image_url" :alt="cat.name" />
            </div>
            <!-- 猫咪头像（无图片时显示占位符） -->
            <div class="cat-avatar placeholder" v-else>
              <span>?</span>
            </div>
            <h3>{{ cat.name }}</h3>
          </div>
          <!-- 卡片主体：喂养记录列表 -->
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
  padding: 40px 20px 80px;
}

.user-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  margin-bottom: 30px;
}

.user-info {
  font-size: 13px;
  color: #666666;
}

.logout-btn {
  padding: 6px 14px;
  border: 1px solid #000000;
  background: #000000;
  color: #ffffff;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #ffffff;
  color: #000000;
}

/* 页头样式 */
.header {
  text-align: center;
  margin-bottom: 80px;
  padding-bottom: 30px;
  border-bottom: 1px solid #000000;
}

/* 主标题样式 */
.header h1 {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 42px;
  font-weight: 300;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

/* 副标题样式 */
.header p {
  font-size: 14px;
  letter-spacing: 0.1em;
  color: #666666;
}

/* 导航卡片容器：flex布局 */
.nav-cards {
  display: flex;
  gap: 16px;
  margin-bottom: 80px;
}

/* 导航卡片样式 */
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

/* 导航卡片悬停效果：反色 */
.card:hover {
  background: #ffffff;
  color: #000000;
}

/* 最新动态区域 */
.latest {
  border-top: 1px solid #000000;
  padding-top: 30px;
}

/* 最新动态标题 */
.latest h2 {
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 24px;
}

/* 猫咪卡片网格布局：响应式 */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

/* 猫咪卡片样式 */
.cat-card {
  border: 1px solid #000000;
  transition: all 0.2s;
}

/* 猫咪卡片悬停效果：上移 + 阴影 */
.cat-card:hover {
  transform: translateY(-4px);
  box-shadow: 4px 4px 0px #000000;
}

/* 卡片头部：头像 + 名字区域 */
.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #eeeeee;
}

/* 猫咪头像容器 */
.cat-avatar {
  width: 48px;
  height: 48px;
  border: 1px solid #000000;
  overflow: hidden;
  flex-shrink: 0;
}

/* 猫咪头像图片 */
.cat-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 猫咪头像占位符 */
.cat-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999999;
  font-size: 20px;
}

/* 猫咪名字 */
.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

/* 卡片主体：喂养记录区域 */
.card-body {
  padding: 12px 16px;
  min-height: 108px;  /* 固定高度，确保卡片对齐 */
}

/* 单条喂养记录 */
.feeding-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #eeeeee;
}

/* 最后一条记录移除底部边框 */
.feeding-item:last-child {
  border-bottom: none;
}

/* 喂养时间 */
.feeding-time {
  font-size: 12px;
  color: #999999;
}

/* 食物类型 */
.feeding-food {
  font-size: 13px;
  color: #000000;
}

/* 空状态样式 */
.empty {
  grid-column: 1 / -1;
  padding: 60px;
  text-align: center;
  color: #999999;
  font-size: 14px;
  border: 1px dashed #dddddd;
}
</style>