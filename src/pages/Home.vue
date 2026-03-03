<template>
  <div class="home-container">
    <!-- Hero Section -->
    <header class="hero">
      <div class="hero-content">
        <h1>Bảo vệ sức khỏe cho bạn và người thân</h1>
        <p class="subtitle">
          Hệ thống Quản lý Tiêm chủng VaxCenter giúp bạn theo dõi lịch tiêm, 
          đặt lịch nhanh chóng và lưu trữ hồ sơ tiêm chủng an toàn.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn btn-primary">Đăng ký ngay</router-link>
          <router-link to="/login" class="btn btn-outline">Tìm hiểu thêm</router-link>
        </div>
      </div>
      <div class="hero-image">
        <div class="image-placeholder">
          <span class="placeholder-icon">🛡️</span>
        </div>
      </div>
    </header>

    <!-- Features Section -->
    <section class="features">
      <div class="section-title">
        <h2>Dịch vụ của chúng tôi</h2>
        <p>Chúng tôi cung cấp các giải pháp quản lý tiêm chủng hiện đại</p>
      </div>

      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Đặt lịch trực tuyến</h3>
          <p>Dễ dàng đặt lịch tiêm chủng tại các trung tâm gần bạn nhất chỉ với vài thao tác.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔔</div>
          <h3>Nhắc lịch tiêm</h3>
          <p>Nhận thông báo nhắc nhở về các mũi tiêm sắp tới để không bao giờ bỏ lỡ.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">📜</div>
          <h3>Hồ sơ điện tử</h3>
          <p>Lưu trữ và tra cứu lịch sử tiêm chủng của bạn và gia đình mọi lúc mọi nơi.</p>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="about">
      <div class="about-container">
        <div class="about-text">
          <h2>Về VaxCenter</h2>
          <p>
            VaxCenter là nền tảng quản lý tiêm chủng hàng đầu, được thiết kế để kết nối người dân 
            với các dịch vụ y tế một cách thuận tiện và hiệu quả nhất.
          </p>
          <p>
            Chúng tôi cam kết bảo mật thông tin y tế của bạn và cung cấp các dữ liệu chính xác 
            về các loại vaccine cũng như lộ trình tiêm chủng khuyến nghị.
          </p>
        </div>
        <div class="about-stats">
          <div class="stat-item">
            <span class="stat-number">1M+</span>
            <span class="stat-label">Người dùng</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">500+</span>
            <span class="stat-label">Trung tâm đối tác</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

/* Hero Section */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 64px 0;
  gap: 64px;
}

.hero-content {
  flex: 1;
}

.hero-content h1 {
  font-size: 56px;
  line-height: 1.2;
  margin-bottom: 24px;
  color: #2c3e50;
}

.subtitle {
  font-size: 20px;
  color: #64748b;
  margin-bottom: 40px;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 12.8px 32px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #137fec;
  color: white;
}

.btn-primary:hover {
  background-color: #0b68c5;
}

.btn-outline {
  border: 2px solid #cbd5e1;
  color: #64748b;
}

.btn-outline:hover {
  border-color: #137fec;
  color: #137fec;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.image-placeholder {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #e2e8f0 0%, #f8fafc 100%);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 20px 20px 60px #d1d5db, -20px -20px 60px #ffffff;
}

.placeholder-icon {
  font-size: 128px;
}

/* Features Section */
.features {
  padding: 96px 0;
}

.section-title {
  text-align: center;
  margin-bottom: 64px;
}

.section-title h2 {
  font-size: 40px;
  margin-bottom: 16px;
}

.section-title p {
  color: #64748b;
  font-size: 17.6px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.feature-card {
  background: white;
  padding: 48px 32px;
  border-radius: 16px;
  text-align: center;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 24px;
}

.feature-card h3 {
  margin-bottom: 16px;
  font-size: 24px;
}

.feature-card p {
  color: #64748b;
}

/* About Section */
.about {
  padding: 96px 0;
  background-color: #f1f5f9;
  margin: 0 -32px;
  padding: 96px 32px;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 64px;
  align-items: center;
}

.about-text {
  flex: 2;
}

.about-text h2 {
  font-size: 40px;
  margin-bottom: 24px;
}

.about-text p {
  margin-bottom: 24px;
  font-size: 17.6px;
  color: #475569;
}

.about-stats {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.stat-item {
  background: white;
  padding: 32px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stat-number {
  display: block;
  font-size: 40px;
  font-weight: 800;
  color: #137fec;
}

.stat-label {
  color: #64748b;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 32px 0;
  }
  .hero-content h1 {
    font-size: 40px;
  }
  .hero-actions {
    justify-content: center;
  }
  .about-container {
    flex-direction: column;
  }
}

@media (max-width: 600px) {
  .image-placeholder {
    width: 280px;
    height: 280px;
  }
  .placeholder-icon {
    font-size: 80px;
  }
}
</style>
