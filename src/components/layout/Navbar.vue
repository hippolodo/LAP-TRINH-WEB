<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo">
        <span class="logo-icon">💉</span>
        <span class="logo-text">VaxCenter</span>
      </router-link>

      <div class="nav-links">
        <router-link to="/login" class="nav-item login-btn">Đăng nhập</router-link>
        <router-link to="/register" class="nav-item register-btn">Đăng ký</router-link>
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
}

.login-btn {
  color: #2c3e50;
  border: 1px solid #2c3e50;
}

.login-btn:hover {
  background-color: #f8f9fa;
}

.register-btn {
  background-color: #137fec;
  color: white;
  border: 1px solid #137fec;
}

.register-btn:hover {
  background-color: #0b68c5;
  border-color: #0b68c5;
}

@media (max-width: 600px) {
  .navbar {
    padding: 16px;
  }
  .logo-text {
    display: none;
  }
}
</style>
