<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const cats = ref([])
const newCat = ref({
  name: '',
  description: '',
  status: '在校'
})
const selectedFile = ref(null)
const fileInputRef = ref(null)
const editingId = ref(null)
const editForm = ref({
  name: '',
  description: '',
  status: ''
})

const getCats = async () => {
  try {
    const response = await request.get('/api/cats')
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
    await request.post('/api/cats', formData, {
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

const startEdit = (cat) => {
  editingId.value = cat.id
  editForm.value = {
    name: cat.name,
    description: cat.description || '',
    status: cat.status
  }
}

const cancelEdit = () => {
  editingId.value = null
  editForm.value = { name: '', description: '', status: '' }
}

const saveEdit = async (catId) => {
  const formData = new FormData()
  formData.append('name', editForm.value.name)
  formData.append('description', editForm.value.description)
  formData.append('status', editForm.value.status)

  try {
    await request.put(`/api/cats/${catId}`, formData)
    editingId.value = null
    getCats()
  } catch (error) {
    console.error('更新猫咪失败:', error)
  }
}

const deleteCat = async (catId) => {
  if (!confirm('确定要删除这只猫咪吗？')) return

  try {
    await request.delete(`/api/cats/${catId}`)
    getCats()
  } catch (error) {
    console.error('删除猫咪失败:', error)
  }
}

onMounted(() => {
  getCats()
})
</script>

<template>
  <div class="page">
    <header class="header">
      <div class="header-row">
        <router-link to="/" class="back">← 返回</router-link>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </div>
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
        <div class="cat-info" v-if="editingId !== cat.id">
          <h3>{{ cat.name }}</h3>
          <p v-if="cat.description">{{ cat.description }}</p>
        </div>
        <div class="edit-form" v-if="editingId === cat.id">
          <input
            v-model="editForm.name"
            type="text"
            class="edit-input"
          />
          <input
            v-model="editForm.description"
            type="text"
            class="edit-input"
          />
          <select v-model="editForm.status" class="edit-select">
            <option value="在校">在校</option>
            <option value="毕业">毕业</option>
          </select>
        </div>
        <div class="actions">
          <span class="status" v-if="editingId !== cat.id">{{ cat.status }}</span>
          <template v-if="editingId === cat.id">
            <button type="button" class="action-btn save" @click="saveEdit(cat.id)">保存</button>
            <button type="button" class="action-btn cancel" @click="cancelEdit">取消</button>
          </template>
          <template v-else>
            <button type="button" class="action-btn" @click="startEdit(cat)">编辑</button>
            <button type="button" class="action-btn" @click="deleteCat(cat.id)">删除</button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  max-width: 700px;
  margin: 0 auto;
  padding: 60px 24px;
}

.header {
  margin-bottom: 48px;
  padding-bottom: 24px;
  border-bottom: 1px solid #000000;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.back {
  font-size: 14px;
  color: #000000;
  text-decoration: none;
}

.back:hover {
  text-decoration: underline;
}

.logout-btn {
  padding: 4px 12px;
  border: 1px solid #000000;
  background: #ffffff;
  color: #000000;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #000000;
  color: #ffffff;
}

.header h1 {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.add-form {
  display: flex;
  gap: 10px;
  margin-bottom: 48px;
  flex-wrap: wrap;
  align-items: center;
}

.form-input,
.form-select {
  flex: 1;
  min-width: 100px;
  height: 40px;
  padding: 0 14px;
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
  padding: 0 14px;
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
  border-top: 1px solid #000000;
}

.cat-item {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  padding: 24px 0;
  border-bottom: 1px solid #eeeeee;
}

.cat-image {
  flex-shrink: 0;
}

.cat-image img {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border: 1px solid #000000;
}

.cat-info {
  flex: 1;
  min-width: 0;
}

.cat-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
}

.cat-info p {
  font-size: 14px;
  color: #666666;
  margin: 0;
}

.edit-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.edit-input,
.edit-select {
  height: 36px;
  padding: 0 12px;
  border: 1px solid #000000;
  background: #ffffff;
  font-size: 14px;
  font-family: inherit;
  border-radius: 0;
  outline: none;
}

.edit-input::placeholder {
  color: #999999;
}

.actions {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.status {
  font-size: 12px;
  padding: 4px 12px;
  border: 1px solid #000000;
  margin-bottom: 4px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 13px;
  color: #666666;
  cursor: pointer;
  padding: 4px 0;
  font-family: inherit;
  text-decoration: underline;
}

.action-btn:hover {
  color: #000000;
}

.action-btn.save {
  color: #000000;
  font-weight: 600;
}

.action-btn.cancel {
  color: #999999;
}

.empty {
  padding: 80px 0;
  text-align: center;
  color: #999999;
  font-size: 14px;
}
</style>