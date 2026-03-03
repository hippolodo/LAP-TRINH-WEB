<script setup>
import Navbar from './components/layout/Navbar.vue'
</script>

<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <footer class="footer">
      <p>&copy; 2024 VaxCenter - Hệ thống Quản lý Tiêm chủng</p>
    </footer>
  </div>
</template>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f8f9fa;
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}

.footer {
  text-align: center;
  padding: 32px;
  background-color: #ffffff;
  border-top: 1px solid #eee;
  color: #6c757d;
  font-size: 14.4px;
}
</style>
