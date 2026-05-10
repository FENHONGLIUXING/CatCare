<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const cats = ref([])
const newCat = ref({
  name: '',
  description: '',
  status: '在校'
})
const selectedFile = ref(null)
const fileInputRef = ref(null)

const getCats = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/cats')
    cats.value = response.data
  } catch (error) {
    console.error('获取猫咪列表失败:', error)
  }
}

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const addCat = async () => {
  if (!newCat.value.name.trim()) return
  
  const formData = new FormData()
  formData.append('name', newCat.value.name)
  formData.append('description', newCat.value.description || '')
  formData.append('status', newCat.value.status)
  if (selectedFile.value) {
    formData.append('file', selectedFile.value)
  }
  
  try {
    await axios.post('http://127.0.0.1:5000/api/cats', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    newCat.value = { name: '', description: '', status: '在校' }
    selectedFile.value = null
    getCats()
  } catch (error) {
    console.error('添加猫咪失败:', error)
  }
}

onMounted(() => {
  getCats()
})
</script>

<template>
  <div class="page">
    <header class="header">
      <router-link to="/" class="back">← 返回</router-link>
      <h1>猫咪档案</h1>
    </header>

    <div class="add-form">
      <input 
        v-model="newCat.name" 
        type="text" 
        placeholder="猫咪名字"
        class="form-input"
      />
      <input 
        v-model="newCat.description" 
        type="text" 
        placeholder="描述（可选）"
        class="form-input"
      />
      <select v-model="newCat.status" class="form-select">
        <option value="在校">在校</option>
        <option value="毕业">毕业</option>
      </select>
      <div class="upload-wrapper">
        <input 
          ref="fileInputRef"
          type="file" 
          accept="image/*" 
          @change="handleFileChange"
          class="file-input-hidden"
        />
        <button type="button" class="upload-btn" @click="triggerFileInput">
          {{ selectedFile ? selectedFile.name : '上传照片' }}
        </button>
      </div>
      <button type="button" class="submit-btn" @click="addCat">添加</button>
    </div>

    <div class="cat-list">
      <div v-if="cats.length === 0" class="empty">
        暂无猫咪记录
      </div>
      <div v-for="cat in cats" :key="cat.id" class="cat-item">
        <div class="cat-image" v-if="cat.image_url">
          <img :src="'http://127.0.0.1:5000' + cat.image_url" :alt="cat.name" />
        </div>
        <div class="cat-info">
          <h3>{{ cat.name }}</h3>
          <p v-if="cat.description">{{ cat.description }}</p>
        </div>
        <span class="status">{{ cat.status }}</span>
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
  gap: 8px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  align-items: center;
}

.form-input,
.form-select {
  flex: 1;
  min-width: 100px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #000000;
  background: #ffffff;
  font-size: 14px;
  font-family: inherit;
  border-radius: 0;
  outline: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.form-input::placeholder {
  color: #999999;
}

.upload-wrapper {
  position: relative;
  flex: 1;
  min-width: 100px;
}

.file-input-hidden {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

.upload-btn {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #000000;
  background: #ffffff;
  color: #000000;
  font-size: 14px;
  font-family: inherit;
  border-radius: 0;
  outline: none;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-btn:hover {
  background: #000000;
  color: #ffffff;
}

.submit-btn {
  min-width: 80px;
  height: 40px;
  padding: 0 20px;
  border: 1px solid #000000;
  background: #000000;
  color: #ffffff;
  font-size: 14px;
  font-family: inherit;
  border-radius: 0;
  outline: none;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover {
  background: #ffffff;
  color: #000000;
}

.cat-list {
  border-top: 1px solid #eeeeee;
}

.cat-item {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  padding: 20px 0;
  border-bottom: 1px solid #eeeeee;
}

.cat-image {
  flex-shrink: 0;
}

.cat-image img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border: 2px solid #000000;
}

.cat-info {
  flex: 1;
}

.cat-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.cat-info p {
  font-size: 14px;
  color: #666666;
}

.status {
  flex-shrink: 0;
  font-size: 12px;
  padding: 4px 12px;
  border: 1px solid #000000;
}

.empty {
  padding: 60px 0;
  text-align: center;
  color: #999999;
  font-size: 14px;
}
</style>