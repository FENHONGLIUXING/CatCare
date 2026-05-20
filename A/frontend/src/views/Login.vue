<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  
  if (!form.value.username.trim() || !form.value.password.trim()) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  
  try {
    await authStore.login(form.value)
    router.push('/')
  } catch (err) {
    if (err.response && err.response.data) {
      error.value = err.response.data.error || '登录失败'
    } else {
      error.value = '网络错误，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}

const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    handleLogin()
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <div class="logo-wrapper">
          <img src="/微信图片_20260520163646_278_69.png" alt="CatCare Logo" class="cat-logo" />
        </div>
        <h1>CatCare</h1>
        <p>校园猫咪社区</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <input
            v-model="form.username"
            type="text"
            placeholder="用户名"
            class="form-input"
            @keypress="handleKeyPress"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <input
            v-model="form.password"
            type="password"
            placeholder="密码"
            class="form-input"
            @keypress="handleKeyPress"
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="tips">
        <p>测试账号：admin / 123456</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 360px;
  padding: 60px 40px;
  border: 1px solid #000000;
  background: #ffffff;
}

.logo {
  text-align: center;
  margin-bottom: 50px;
}

.logo-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}

.cat-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.logo h1 {
  font-size: 32px;
  font-weight: 300;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.logo p {
  font-size: 13px;
  letter-spacing: 0.1em;
  color: #666666;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  width: 100%;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border: 1px solid #000000;
  background: #ffffff;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: #999999;
}

.form-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  color: #d9534f;
  font-size: 13px;
  text-align: center;
  padding: 10px;
  border: 1px solid #f8d7da;
  background: #fff5f5;
}

.login-btn {
  width: 100%;
  height: 48px;
  background: #000000;
  color: #ffffff;
  border: 1px solid #000000;
  font-size: 15px;
  font-family: inherit;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn:hover:not(:disabled) {
  background: #ffffff;
  color: #000000;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tips {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eeeeee;
  text-align: center;
}

.tips p {
  font-size: 12px;
  color: #999999;
}
</style>
