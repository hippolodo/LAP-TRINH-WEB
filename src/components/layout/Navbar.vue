<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  alert('Đã đăng xuất thành công!')
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo">
        <span class="logo-icon">💉</span>
        <span class="logo-text">VaxCenter</span>
      </router-link>

      <div class="nav-links">
        <template v-if="authStore.user?.role === 'staff'">
          <router-link to="/" class="nav-item">Bảng điều khiển</router-link>
          <router-link to="/products" class="nav-item">Kho dược</router-link>
        </template>
        <template v-else>
          <router-link to="/products" class="nav-item">Tra cứu Vaccine</router-link>
        </template>

        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="nav-item login-btn">Đăng nhập</router-link>
          <router-link to="/register" class="nav-item register-btn">Đăng ký</router-link>
        </template>
        <template v-else>
          <span class="user-welcome">Chào, {{ authStore.user?.name }}</span>
          <template v-if="authStore.user?.role !== 'staff'">
            <router-link to="/my-appointments" class="nav-item">Lịch hẹn</router-link>
          </template>
          <router-link to="/profile" class="nav-item">Hồ sơ</router-link>
          <button @click="handleLogout" class="nav-item logout-btn">Đăng xuất</button>
        </template>
      </div>

    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 16px 32px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.nav-links {
  display: flex;
  gap: 16px;
  align-items: center;
}

.nav-item {
  text-decoration: none;
  padding: 8px 19.2px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: #2c3e50;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
}

.nav-item:hover {
  color: #137fec;
}

.user-welcome {
  font-weight: 600;
  color: #137fec;
}

.login-btn {
  color: #2c3e50;
  border: 1px solid #2c3e50;
}

.login-btn:hover {
  background-color: #f8f9fa;
  color: #137fec;
}

.register-btn {
  background-color: #137fec;
  color: white;
  border: 1px solid #137fec;
}

.register-btn:hover {
  background-color: #0b68c5;
  border-color: #0b68c5;
  color: white;
}

.logout-btn {
  color: #dc3545;
}

.logout-btn:hover {
  background-color: #fff5f5;
  color: #c82333;
}

@media (max-width: 600px) {
  .navbar {
    padding: 16px;
  }
  .logo-text {
    display: none;
  }
  .nav-links {
    gap: 8px;
  }
  .nav-item {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>
