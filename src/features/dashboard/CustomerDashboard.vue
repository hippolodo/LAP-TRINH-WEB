<script setup>
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()

const upcomingAppointments = [
  { id: 1, vaccine: 'Vaccine Cúm Tứ giá', date: '2024-03-20', location: 'VaxCenter Quận 1' },
  { id: 2, vaccine: 'Vaccine Phế cầu', date: '2024-04-15', location: 'VaxCenter Quận 7' }
]

const recentHistory = [
  { id: 101, vaccine: 'Vaccine Viêm gan B', date: '2023-12-10', result: 'Đã tiêm' },
  { id: 102, vaccine: 'Vaccine HPV', date: '2023-11-05', result: 'Đã tiêm' }
]

const recommendedVaccines = [
  { id: 1, name: 'Vaccine Ung thư cổ tử cung (HPV)', price: '1,790,000đ', image: '💉' },
  { id: 2, name: 'Vaccine Viêm não Nhật Bản', price: '250,000đ', image: '🧪' },
  { id: 3, name: 'Vaccine Thủy đậu', price: '750,000đ', image: '🦠' }
]
</script>

<template>
  <div class="dashboard">
    <header class="welcome-banner">
      <div class="banner-content">
        <h1>Chào mừng trở lại, {{ authStore.user?.name }}!</h1>
        <p>Hôm nay bạn muốn thực hiện dịch vụ nào?</p>
        <div class="quick-actions">
          <router-link to="/appointments" class="action-btn primary">
            <span class="icon">📅</span> Đặt lịch tiêm
          </router-link>
          <router-link to="/products" class="action-btn secondary">
            <span class="icon">🔍</span> Tra cứu vaccine
          </router-link>
        </div>
      </div>
      <div class="banner-stats">
        <div class="mini-stat">
          <span class="stat-value">2</span>
          <span class="stat-label">Lịch hẹn sắp tới</span>
        </div>
        <div class="mini-stat">
          <span class="stat-value">12</span>
          <span class="stat-label">Mũi đã tiêm</span>
        </div>
      </div>
    </header>

    <div class="dashboard-grid">
      <!-- Left Column: Appointments and History -->
      <div class="main-content">
        <section class="section-card">
          <div class="section-header">
            <h2>Lịch hẹn sắp tới</h2>
            <router-link to="/my-appointments" class="view-all">Xem tất cả</router-link>
          </div>
          <div class="list-container">
            <div v-for="apt in upcomingAppointments" :key="apt.id" class="list-item appointment">
              <div class="item-icon">📅</div>
              <div class="item-info">
                <h4>{{ apt.vaccine }}</h4>
                <p>{{ apt.location }} • {{ apt.date }}</p>
              </div>
              <button class="btn-sm">Chi tiết</button>
            </div>
          </div>
        </section>

        <section class="section-card">
          <div class="section-header">
            <h2>Lịch sử tiêm chủng gần đây</h2>
            <router-link to="/history" class="view-all">Xem tất cả</router-link>
          </div>
          <div class="list-container">
            <div v-for="hist in recentHistory" :key="hist.id" class="list-item history">
              <div class="item-icon">✅</div>
              <div class="item-info">
                <h4>{{ hist.vaccine }}</h4>
                <p>Ngày tiêm: {{ hist.date }}</p>
              </div>
              <span class="status-badge">{{ hist.result }}</span>
            </div>
          </div>
        </section>
      </div>

      <!-- Right Column: Recommendations -->
      <div class="sidebar">
        <section class="section-card">
          <div class="section-header">
            <h2>Gợi ý cho bạn</h2>
          </div>
          <div class="recommendations">
            <div v-for="vax in recommendedVaccines" :key="vax.id" class="vax-card">
              <span class="vax-icon">{{ vax.image }}</span>
              <div class="vax-details">
                <h4>{{ vax.name }}</h4>
                <p class="price">{{ vax.price }}</p>
                <button class="btn-book">Chọn tiêm</button>
              </div>
            </div>
          </div>
        </section>

        <section class="info-card">
          <h3>Thông tin y tế</h3>
          <p>Luôn cập nhật thông tin cá nhân để chúng tôi có thể đưa ra lộ trình tiêm chủng chính xác nhất.</p>
          <router-link to="/profile" class="btn-link">Cập nhật ngay →</router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding-bottom: 64px;
}

/* Welcome Banner */
.welcome-banner {
  background: linear-gradient(135deg, #137fec 0%, #0b68c5 100%);
  color: white;
  padding: 48px;
  border-radius: 20px;
  margin-bottom: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 10px 25px rgba(19, 127, 236, 0.2);
}

.banner-content h1 {
  font-size: 32px;
  margin-bottom: 12px;
}

.banner-content p {
  opacity: 0.9;
  font-size: 18px;
  margin-bottom: 32px;
}

.quick-actions {
  display: flex;
  gap: 16px;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.action-btn.primary {
  background: white;
  color: #137fec;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.banner-stats {
  display: flex;
  gap: 24px;
}

.mini-stat {
  background: rgba(255, 255, 255, 0.15);
  padding: 20px;
  border-radius: 16px;
  text-align: center;
  min-width: 120px;
  backdrop-filter: blur(10px);
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 20px;
  color: #2c3e50;
}

.view-all {
  color: #137fec;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.item-icon {
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  margin-bottom: 4px;
  color: #334155;
}

.item-info p {
  font-size: 14px;
  color: #64748b;
}

.status-badge {
  background: #dcfce7;
  color: #166534;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.btn-sm {
  padding: 6px 12px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

/* Sidebar */
.vax-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.vax-card:last-child {
  border-bottom: none;
}

.vax-icon {
  font-size: 32px;
}

.vax-details h4 {
  font-size: 15px;
  margin-bottom: 4px;
}

.price {
  color: #137fec;
  font-weight: 700;
  font-size: 14px;
  margin-bottom: 8px;
}

.btn-book {
  background: #f1f5f9;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  color: #475569;
}

.btn-book:hover {
  background: #137fec;
  color: white;
}

.info-card {
  background: #fefce8;
  border: 1px solid #fef08a;
  border-radius: 16px;
  padding: 24px;
}

.info-card h3 {
  color: #854d0e;
  margin-bottom: 12px;
  font-size: 18px;
}

.info-card p {
  color: #713f12;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
}

.btn-link {
  color: #854d0e;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .welcome-banner {
    flex-direction: column;
    text-align: center;
    padding: 32px 24px;
  }
  .banner-stats {
    margin-top: 32px;
    width: 100%;
    justify-content: center;
  }
  .quick-actions {
    justify-content: center;
  }
}
</style>
