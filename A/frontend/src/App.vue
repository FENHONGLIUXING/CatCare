<script setup>
import { ref } from 'vue'
import axios from 'axios'

const count = ref(0)
const backendmessage = ref('')
const addcount = async () => {
  count.value++
  if (count.value === 5) {
    try {
      const response = await axios.get('http://localhost:5000/api/test')
      backendmessage.value = response.data.message
    } catch (error) {
      alert('Failed to fetch message from backend.')
    }
  }
  if (count.value >= 10) {
    alert('Count has reached 10!')
    count.value = 0
  }
  }


</script>

<template>
  <button @click="addcount">Click me!</button>
  <p>Count: {{ count }}</p>
  <p>后端来电： {{ backendmessage }}</p>
</template>

<style scoped></style>
