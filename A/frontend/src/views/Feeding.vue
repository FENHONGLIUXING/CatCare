<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const cats = ref([])
const records = ref([])
const newRecord = ref({
  cat_id: '',
  food_type: '',
  time: ''
})

const getCats = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/cats')
    cats.value = response.data
  } catch (error) {
    console.error('获取猫咪列表失败:', error)
  }
}

const getRecords = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/feeding')
    records.value = response.data
  } catch (error) {
    console.error('获取投喂记录失败:', error)
  }
}

const addRecord = async () => {
  if (!newRecord.value.cat_id || !newRecord.value.food_type) return
  
  try {
    await axios.post('http://127.0.0.1:5000/api/feeding', newRecord.value)
    newRecord.value = { cat_id: '', food_type: '', time: '' }
    getRecords()
  } catch (error) {
    console.error('添加投喂记录失败:', error)
  }
}

const getCatName = (catId) => {
  const cat = cats.value.find(c => c.id === catId)
  return cat ? cat.name : '未知'
}

onMounted(() => {
  getCats()
  getRecords()
})
</script>

<template>
  <div class="page">
    <header class="header">
      <router-link to="/" class="back">← 返回</router-link>
      <h1>投喂记录</h1>
    </header>

    <div class="add-form">
      <select v-model="newRecord.cat_id">
        <option value="">选择猫咪</option>
        <option v-for="cat in cats" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <input 
        v-model="newRecord.food_type" 
        type="text" 
        placeholder="食物类型"
        @keyup.enter="addRecord"
      />
      <input 
        v-model="newRecord.time" 
        type="datetime-local" 
      />
      <button @click="addRecord">添加</button>
    </div>

    <div class="record-list">
      <div v-if="records.length === 0" class="empty">
        暂无投喂记录
      </div>
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
.page {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #000000;
}

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

.add-form {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.add-form select,
.add-form input {
  flex: 1;
  min-width: 120px;
  padding: 12px;
  border: 1px solid #000000;
  background: #ffffff;
  font-size: 14px;
  outline: none;
}

.add-form input::placeholder {
  color: #999999;
}

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

.record-list {
  border-top: 1px solid #eeeeee;
}

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

.time {
  font-size: 12px;
  color: #999999;
}

.empty {
  padding: 60px 0;
  text-align: center;
  color: #999999;
  font-size: 14px;
}
</style>