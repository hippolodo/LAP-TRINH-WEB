<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import VaccinationRecord from '../features/profile/VaccinationRecord.vue'

const router = useRouter()
const authStore = useAuthStore()
const user = authStore.user
const isStaff = user?.role === 'staff'

// Mock extra data if not present in store
const userDetails = ref({
  age: isStaff ? 38 : 25,
  gender: isStaff ? 'Nam' : 'Nam',
  phone: isStaff ? '0912.345.678' : '0988.777.666',
  workLocation: isStaff ? 'VaxCenter Quận 1' : null,
  address: isStaff ? null : '123 Đường ABC, Quận 3, TP.HCM'
})

const activeTab = ref('info')

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
            <span class="avatar-placeholder">{{ user?.name?.charAt(0) }}</span>
          </div>
          <h2 class="user-name">{{ user?.name }}</h2>
          <p class="user-role-tag">{{ isStaff ? 'Nhân viên Y tế' : 'Khách hàng' }}</p>
          
          <div class="user-summary">
            <div class="summary-item">
              <span class="s-label">Email</span>
              <span class="s-value">{{ user?.email }}</span>
            </div>
            <div class="summary-item">
              <span class="s-label">Số điện thoại</span>
              <span class="s-value">{{ userDetails.phone }}</span>
            </div>
          </div>
        </div>

        <nav class="profile-nav-menu">
          <button 
            @click="activeTab = 'info'" 
            :class="['menu-item', activeTab === 'info' ? 'active' : '']"
          >
            <span class="m-icon">👤</span> Thông tin tài khoản
          </button>
          <button 
            v-if="!isStaff"
            @click="activeTab = 'records'" 
            :class="['menu-item', activeTab === 'records' ? 'active' : '']"
          >
            <span class="m-icon">📘</span> Sổ tiêm chủng
          </button>
          <!-- <button class="menu-item">
            <span class="m-icon">🛡️</span> Bảo mật & mật khẩu
          </button> -->
          <button @click="handleLogout" class="menu-item logout-item">
            <span class="m-icon">🚪</span> Đăng xuất
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="profile-main-content">
        <!-- Account Info View -->
        <div v-if="activeTab === 'info'" class="info-card-container">
          <div class="info-header">
            <h3>Hồ sơ cá nhân</h3>
            <button class="btn-edit">Chỉnh sửa</button>
          </div>
          
          <div class="info-grid">
            <div class="info-item">
              <label>Họ và tên</label>
              <p>{{ user?.name }}</p>
            </div>
            <div class="info-item">
              <label>Email</label>
              <p>{{ user?.email }}</p>
            </div>
            <div class="info-item">
              <label>Số điện thoại</label>
              <p>{{ userDetails.phone }}</p>
            </div>
            <div class="info-item">
              <label>Tuổi</label>
              <p>{{ userDetails.age }} tuổi</p>
            </div>
            <div class="info-item">
              <label>Giới tính</label>
              <p>{{ userDetails.gender }}</p>
            </div>
            
            <!-- Staff specific -->
            <div v-if="isStaff" class="info-item full-width highlight">
              <label>Cơ sở làm việc</label>
              <p>{{ userDetails.workLocation }}</p>
            </div>
            
            <!-- Customer specific -->
            <div v-if="!isStaff" class="info-item full-width">
              <label>Địa chỉ thường trú</label>
              <p>{{ userDetails.address }}</p>
            </div>
          </div>
        </div>

        <!-- Vaccination Records View (Customers Only) -->
        <div v-if="activeTab === 'records' && !isStaff">
          <VaccinationRecord />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  background-color: #f8fafc;
  min-height: calc(100vh - 80px);
  padding: 40px 0;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 32px;
}

/* Sidebar Styles */
.user-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  margin-bottom: 24px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #137fec 0%, #0b68c5 100%);
  border-radius: 32px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  font-size: 40px;
  color: white;
  font-weight: 700;
}

.user-name {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.user-role-tag {
  font-size: 14px;
  font-weight: 600;
  color: #137fec;
  background: #eff6ff;
  display: inline-block;
  padding: 6px 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.user-summary {
  text-align: left;
  border-top: 1px solid #f1f5f9;
  padding-top: 24px;
}

.summary-item {
  margin-bottom: 16px;
}

.s-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.s-value {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

/* Nav Menu */
.profile-nav-menu {
  background: white;
  border-radius: 24px;
  padding: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  color: #64748b;
  border-radius: 16px;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.2s;
  width: 100%;
  border: none;
  background: none;
  cursor: pointer;
  margin-bottom: 4px;
}

.menu-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.menu-item.active {
  background: #137fec;
  color: white;
}

.logout-item {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
  color: #ef4444;
}

.logout-item:hover {
  background: #fef2f2;
  color: #dc2626;
}

/* Main Content Styles */
.info-card-container {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f1f5f9;
}

.info-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.btn-edit {
  background: #f1f5f9;
  color: #475569;
  border: none;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit:hover {
  background: #e2e8f0;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.info-item label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.info-item p {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
}

.full-width {
  grid-column: span 2;
}

.highlight p {
  color: #137fec;
  font-size: 18px;
}

@media (max-width: 1024px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}
</style>
