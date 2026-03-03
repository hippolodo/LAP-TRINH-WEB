<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const handleLogin = () => {
  console.log('Đăng nhập với:', { email: email.value, password: password.value })
  alert(`Đang đăng nhập với email: ${email.value}`)
  // Tại đây bạn sẽ gọi API từ authApi.js
}
</script>

<template>
  <div class="login-container">
    <h3>Đăng Nhập Hệ Thống</h3>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email:</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          placeholder="nhập email của bạn" 
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Mật khẩu:</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          placeholder="nhập mật khẩu" 
          required
        />
      </div>
      <button type="submit" class="btn-login">Đăng Nhập</button>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h3 {
  width: 500px;
  text-align: center; 
  color: 137fec;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 60%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Quan trọng để input không bị tràn */
}

.btn-login {
  width: 100%;
  padding: 10px;
  background-color: #137fec;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-login:hover {
  background-color: #137fec;
}
</style>
