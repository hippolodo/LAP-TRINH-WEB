<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import VaccinationRecord from '../features/profile/VaccinationRecord.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- Sidebar / User Info -->
      <aside class="profile-sidebar">
        <div class="user-card">
          <div class="user-avatar">
            <span class="avatar-placeholder">{{ authStore.user?.name?.charAt(0) }}</span>
          </div>
          <h2 class="user-name">{{ authStore.user?.name }}</h2>
          <p class="user-id-tag">ID: BN-10928</p>
          
          <div class="user-meta-list">
            <div class="meta-row">
              <span class="m-label">Email</span>
              <span class="m-value">{{ authStore.user?.email }}</span>
            </div>
            <div class="meta-row">
              <span class="m-label">Ngày sinh</span>
              <span class="m-value">15/05/1995</span>
            </div>
            <div class="meta-row">
              <span class="m-label">Giới tính</span>
              <span class="m-value">Nam</span>
            </div>
          </div>
          <button class="btn-primary-outline">Chỉnh sửa hồ sơ</button>
        </div>

        <nav class="profile-nav-menu">
          <a href="#" class="menu-item active">
            <span class="m-icon">📘</span> Sổ tiêm chủng
          </a>
          <a href="#" class="menu-item">
            <span class="m-icon">👤</span> Thông tin tài khoản
          </a>
          <a href="#" class="menu-item">
            <span class="m-icon">🛡️</span> Bảo mật & mật khẩu
          </a>
          <button @click="handleLogout" class="menu-item logout-item">
            <span class="m-icon">🚪</span> Đăng xuất
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="profile-main-content">
        <VaccinationRecord />
      </main>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  background-color: #f7fafc;
  min-height: calc(100vh - 80px);
  padding: 40px 0;
}

.profile-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
}

/* Sidebar Styles */
.user-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  border: 1px solid #edf2f7;
  margin-bottom: 24px;
}

.user-avatar {
  width: 110px;
  height: 110px;
  background: linear-gradient(135deg, #137fec 0%, #0b68c5 100%);
  border-radius: 35px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 15px rgba(19, 127, 236, 0.2);
}

.avatar-placeholder {
  font-size: 48px;
  color: white;
  font-weight: 800;
}

.user-name {
  font-size: 20px;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 6px;
}

.user-id-tag {
  font-size: 13px;
  font-weight: 700;
  color: #a0aec0;
  background: #f7fafc;
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 24px;
}

.user-meta-list {
  text-align: left;
  border-top: 1px solid #f1f5f9;
  padding-top: 24px;
  margin-bottom: 24px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 14px;
  font-size: 14px;
}

.meta-row .m-label { color: #a0aec0; font-weight: 600; }
.meta-row .m-value { color: #4a5568; font-weight: 700; }

.btn-primary-outline {
  width: 100%;
  padding: 12px;
  background: white;
  border: 2px solid #137fec;
  color: #137fec;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary-outline:hover {
  background: #137fec;
  color: white;
}

/* Nav Menu */
.profile-nav-menu {
  background: white;
  border-radius: 20px;
  padding: 10px;
  border: 1px solid #edf2f7;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  text-decoration: none;
  color: #718096;
  border-radius: 14px;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.2s;
  width: 100%;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
}

.menu-item:hover {
  background: #f7fafc;
  color: #137fec;
}

.menu-item.active {
  background: #ebf8ff;
  color: #137fec;
}

.logout-item {
  margin-top: 10px;
  border-top: 1px solid #f7fafc;
  color: #e53e3e;
}

.logout-item:hover {
  background: #fff5f5;
  color: #c53030;
}

@media (max-width: 1024px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}
</style>
