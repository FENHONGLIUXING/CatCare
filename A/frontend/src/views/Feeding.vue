<script setup>
// 导入 Vue 组合式 API 和 Axios
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 响应式数据：猫咪列表、投喂记录列表、新记录表单数据
const cats = ref([])
const records = ref([])
const newRecord = ref({
  cat_id: '',      // 选中的猫咪ID
  food_type: '',   // 食物类型
  time: ''         // 投喂时间（可选，默认当前时间）
})

// 获取猫咪列表（用于下拉选择）
const getCats = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/cats')
    cats.value = response.data
  } catch (error) {
    console.error('获取猫咪列表失败:', error)
  }
}

// 获取最近100条投喂记录（按时间倒序）
const getRecords = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/feeding')
    records.value = response.data
  } catch (error) {
    console.error('获取投喂记录失败:', error)
  }
}

// 添加新的投喂记录
const addRecord = async () => {
  // 验证必填字段
  if (!newRecord.value.cat_id || !newRecord.value.food_type) return
  
  try {
    await axios.post('http://127.0.0.1:5000/api/feeding', newRecord.value)
    // 重置表单
    newRecord.value = { cat_id: '', food_type: '', time: '' }
    // 刷新记录列表
    getRecords()
  } catch (error) {
    console.error('添加投喂记录失败:', error)
  }
}

// 根据猫咪ID获取猫咪名称（辅助函数）
const getCatName = (catId) => {
  const cat = cats.value.find(c => c.id === catId)
  return cat ? cat.name : '未知'
}

// 组件挂载时初始化数据
onMounted(() => {
  getCats()
  getRecords()
})
</script>

<template>
  <!-- 页面主容器 -->
  <div class="page">
    <!-- 页头：返回链接 + 标题 -->
    <header class="header">
      <router-link to="/" class="back">← 返回</router-link>
      <h1>投喂记录</h1>
    </header>

    <!-- 添加投喂记录表单 -->
    <div class="add-form">
      <!-- 猫咪选择下拉框 -->
      <select v-model="newRecord.cat_id">
        <option value="">选择猫咪</option>
        <option v-for="cat in cats" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <!-- 食物类型输入框 -->
      <input 
        v-model="newRecord.food_type" 
        type="text" 
        placeholder="食物类型"
        @keyup.enter="addRecord"  <!-- 回车键提交 -->
      />
      <!-- 投喂时间选择（可选） -->
      <input 
        v-model="newRecord.time" 
        type="datetime-local" 
      />
      <!-- 添加按钮 -->
      <button @click="addRecord">添加</button>
    </div>

    <!-- 投喂记录列表 -->
    <div class="record-list">
      <!-- 空状态提示 -->
      <div v-if="records.length === 0" class="empty">
        暂无投喂记录
      </div>
      <!-- 记录项循环渲染 -->
      <div v-for="record in records" :key="record.id" class="record-item">
        <div class="record-info">
          <h3>{{ getCatName(record.cat_id) }}</h3>
          <p>{{ record.food_type }}</p>
        </div>
        <span class="time">{{ record.time }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面容器：居中限宽 */
.page {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* 页头样式 */
.header {
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #000000;
}

/* 返回链接 */
.back {
  font-size: 14px;
  color: #000000;
  text-decoration: none;
  margin-bottom: 10px;
  display: inline-block;
}

.back:hover {
  text-decoration: underline;
}

.header h1 {
  font-size: 24px;
  font-weight: 700;
}

/* 表单容器：flex布局 */
.add-form {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

/* 表单控件样式：统一高度、边框 */
.add-form select,
.add-form input {
  flex: 1;
  min-width: 120px;
  padding: 12px;
  border: 1px solid #000000;
  background: #ffffff;
  font-size: 14px;
  outline: none;  /* 移除默认焦点描边 */
}

.add-form input::placeholder {
  color: #999999;
}

/* 添加按钮样式 */
.add-form button {
  padding: 12px 24px;
  background: #000000;
  color: #ffffff;
  border: none;
  font-size: 14px;
  cursor: pointer;
}

.add-form button:hover {
  background: #333333;
}

/* 记录列表容器 */
.record-list {
  border-top: 1px solid #eeeeee;
}

/* 单条记录项 */
.record-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 0;
  border-bottom: 1px solid #eeeeee;
}

.record-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.record-info p {
  font-size: 14px;
  color: #666666;
}

/* 时间显示 */
.time {
  font-size: 12px;
  color: #999999;
}

/* 空状态样式 */
.empty {
  padding: 60px 0;
  text-align: center;
  color: #999999;
  font-size: 14px;
}
</style>