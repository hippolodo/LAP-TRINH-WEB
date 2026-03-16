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
      <!-- 1. Logo bên trái -->
      <router-link to="/" class="logo">
        <span class="logo-icon">💉</span>
        <span class="logo-text">VaxCenter</span>
      </router-link>

      <!-- 2. Câu chào dịch sang trái -->
      <span v-if="authStore.isAuthenticated" class="user-welcome">
        Chào, {{ authStore.user?.name }} ({{ authStore.user?.role?.toUpperCase() }})
      </span>

      <!-- 3. Các link điều hướng đẩy về bên phải -->
      <div class="nav-links">
        <!-- Links for Admin -->
        <template v-if="authStore.user?.role === 'admin'">
          <router-link to="/" class="nav-item">Bảng quản trị</router-link>
          <router-link to="/products" class="nav-item">Kho vaccine</router-link>
        </template>
        
        <!-- Links for Staff -->
        <template v-else-if="authStore.user?.role === 'staff'">
          <router-link to="/" class="nav-item">Bảng điều khiển</router-link>
          <router-link to="/products" class="nav-item">Kho dược</router-link>
        </template>
        
        <!-- Links for Customer/Guest -->
        <template v-else>
          <router-link to="/products" class="nav-item">Tra cứu Vaccine</router-link>
        </template>

        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="nav-item login-btn">Đăng nhập</router-link>
          <router-link to="/register" class="nav-item register-btn">Đăng ký</router-link>
        </template>
        <template v-else>
          <template v-if="authStore.user?.role === 'customer'">
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
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 8px;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.user-welcome {
  font-weight: 600;
  color: #137fec;
  margin-right: auto; /* Đẩy nav-links sang bên phải */
  font-size: 16px;
  padding-left: 12px;
  border-left: 2px solid #e2e8f0;
}

.nav-links {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-item {
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
  color: #475569;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 15px;
}

.nav-item:hover {
  color: #137fec;
  background-color: #f1f5f9;
}

.login-btn {
  color: #137fec;
  border: 1px solid #137fec;
}

.register-btn {
  background-color: #137fec;
  color: white;
}

.register-btn:hover {
  background-color: #0b68c5;
  color: white;
}

.logout-btn {
  color: #dc3545;
}

.logout-btn:hover {
  background-color: #fff5f5;
  color: #c82333;
}

@media (max-width: 768px) {
  .navbar {
    padding: 16px;
  }
  .logo-text, .user-welcome {
    display: none; /* Ẩn câu chào trên mobile để tránh chật chội */
  }
  .nav-links {
    gap: 4px;
  }
  .nav-item {
    padding: 8px;
    font-size: 13px;
  }
}
</style>
