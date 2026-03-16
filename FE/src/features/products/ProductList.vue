<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../store/auth'

import productApi from '../../api/productApi'

const authStore = useAuthStore()
const isAdmin = authStore.user?.role === 'admin'
const isStaff = authStore.user?.role === 'staff'
const staffLocation = authStore.user?.workLocation || 'VaxCenter Quận 1'

const loading = ref(true)
const searchQuery = ref('')
const selectedCenter = ref('Tất cả')

const centerOptions = [
  'Tất cả', 'VaxCenter Quận 1', 'VaxCenter Quận 3', 'VaxCenter Quận 7', 'VaxCenter Bình Thạnh', 'VaxCenter Thủ Đức'
]

// Dữ liệu tồn kho
const inventoryData = ref([])

const fetchInventory = async () => {
  loading.value = true
  try {
    const response = await productApi.getInventory()
    inventoryData.value = response.data.map(item => ({
      id: item.id,
      name: item.vaccine?.name || 'Unknown',
      manufacturer: item.vaccine?.manufacturer || 'Unknown',
      price: item.vaccine?.price ? `${item.vaccine.price.toLocaleString()} VNĐ` : '0 VNĐ',
      location: item.location?.name || 'Unknown',
      stock: item.stock_quantity,
      batch: item.batch_number,
      description: item.vaccine?.description || ''
    }))
  } catch (error) {
    console.error("Lỗi khi tải dữ liệu kho:", error)
  } finally {
    loading.value = false
  }
}

// Logic lọc cho Admin và Staff
const filteredInventory = computed(() => {
  let data = inventoryData.value

  // Nếu là Staff, chỉ xem kho của cơ sở mình
  if (isStaff) {
    data = data.filter(item => item.location === staffLocation)
  } 
  // Nếu là Admin, lọc theo dropdown cơ sở
  else if (isAdmin && selectedCenter.value !== 'Tất cả') {
    data = data.filter(item => item.location === selectedCenter.value)
  }
  // Nếu là khách hàng, gộp các loại vaccine trùng tên để tránh hiển thị lặp theo cơ sở
  else if (!isAdmin && !isStaff) {
    const uniqueVaccines = []
    const seenNames = new Set()
    
    data.forEach(item => {
      if (!seenNames.has(item.name)) {
        uniqueVaccines.push(item)
        seenNames.add(item.name)
      }
    })
    data = uniqueVaccines
  }

  // Lọc theo từ khóa tìm kiếm
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(item => 
      item.name.toLowerCase().includes(q) || 
      (item.batch && item.batch.toLowerCase().includes(q))
    )
  }

  return data
})

// Thống kê tổng hợp cho Admin
const centerStats = computed(() => {
  const stats = {}
  inventoryData.value.forEach(item => {
    if (!stats[item.location]) {
      stats[item.location] = { total: 0, lowStock: 0 }
    }
    stats[item.location].total += item.stock
    if (item.stock < 20) stats[item.location].lowStock++
  })
  return stats
})

onMounted(() => {
  fetchInventory()
})
</script>

<template>
  <div class="product-lookup">
    <header class="page-header">
      <h1>{{ isAdmin ? 'Thống kê Kho Toàn Hệ Thống' : (isStaff ? 'Kho Vaccine - ' + staffLocation : 'Tra cứu Vaccine') }}</h1>
      <p v-if="isAdmin">Quản lý và theo dõi phân phối vaccine tại tất cả các trung tâm</p>
    </header>

    <!-- Admin Overview Cards -->
    <div v-if="isAdmin" class="admin-stats-grid">
      <div v-for="(stat, center) in centerStats" :key="center" class="stat-card">
        <h4>{{ center }}</h4>
        <div class="stat-main">
          <span class="stat-number">{{ stat.total }}</span>
          <span class="stat-unit">liều</span>
        </div>
        <p :class="{alert: stat.lowStock > 0}">
          {{ stat.lowStock > 0 ? `⚠️ ${stat.lowStock} loại sắp hết` : '✅ Kho ổn định' }}
        </p>
      </div>
    </div>

    <div class="controls-container">
      <div class="search-bar">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm tên vaccine hoặc số lô..."
          class="search-input"
        >
      </div>
      
      <div v-if="isAdmin" class="filter-group">
        <label>Lọc theo cơ sở:</label>
        <select v-model="selectedCenter" class="center-select">
          <option v-for="opt in centerOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Đang tải dữ liệu kho...</p>
    </div>

    <div v-else class="inventory-table-container">
      <table class="inventory-table">
        <thead>
          <tr>
            <th>Vaccine</th>
            <th v-if="isAdmin">Cơ sở</th>
            <th v-if="isAdmin || isStaff">Số lô</th>
            <th v-if="isAdmin || isStaff">Tồn kho</th>
            <th v-if="isAdmin || isStaff">Tình trạng</th>
            <th v-if="!isAdmin && !isStaff">Giá</th>
            <th v-if="!isAdmin && !isStaff">Công dụng</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredInventory" :key="item.id">
            <td>
              <div class="name-cell">
                <strong>{{ item.name }}</strong>
                <span>{{ item.manufacturer }}</span>
              </div>
            </td>
            <td v-if="isAdmin">
              <span class="location-tag">{{ item.location }}</span>
            </td>
            <td v-if="isAdmin || isStaff"><code>{{ item.batch }}</code></td>
            <td v-if="isAdmin || isStaff">
              <span :class="['stock-value', item.stock < 20 ? 'danger' : '']">
                {{ item.stock }} liều
              </span>
            </td>
            <td v-if="isAdmin || isStaff">
              <div class="progress-container">
                <div class="progress-bar" :style="{ width: Math.min(item.stock, 100) + '%', backgroundColor: item.stock < 20 ? '#ef4444' : '#10b981' }"></div>
              </div>
            </td>
            <td v-if="!isAdmin && !isStaff" class="price-cell">
              {{ item.price }}
            </td>
            <td v-if="!isAdmin && !isStaff" class="description-cell">
              {{ item.description }}
            </td>
          </tr>
          <tr v-if="filteredInventory.length === 0">
            <td :colspan="isAdmin ? 5 : (isStaff ? 4 : 3)" class="no-data">Không tìm thấy dữ liệu phù hợp.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.product-lookup {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  margin-bottom: 32px;
  text-align: center;
}

.page-header h1 { font-size: 32px; color: #1e293b; margin-bottom: 8px; }
.page-header p { color: #64748b; font-size: 18px; }

/* Admin Stats Cards */
.admin-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #137fec;
}

.stat-card h4 { font-size: 14px; color: #64748b; margin-bottom: 12px; }
.stat-main { display: flex; align-items: baseline; gap: 4px; margin-bottom: 8px; }
.stat-number { font-size: 28px; font-weight: 800; color: #1e293b; }
.stat-unit { font-size: 14px; color: #94a3b8; font-weight: 600; }
.stat-card p { font-size: 13px; font-weight: 600; color: #10b981; }
.stat-card p.alert { color: #ef4444; }

/* Controls */
.controls-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.search-bar { position: relative; flex: 1; max-width: 500px; }
.search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.search-input {
  width: 100%; padding: 12px 16px 12px 48px;
  border: 2px solid #e2e8f0; border-radius: 12px;
  font-size: 15px; outline: none; transition: all 0.3s;
}
.search-input:focus { border-color: #137fec; box-shadow: 0 0 0 4px rgba(19, 127, 236, 0.1); }

.filter-group { display: flex; align-items: center; gap: 12px; }
.filter-group label { font-weight: 700; color: #475569; font-size: 14px; }
.center-select {
  padding: 10px 16px; border: 2px solid #e2e8f0; border-radius: 12px;
  background: white; font-weight: 600; color: #1e293b; cursor: pointer;
}

/* Table */
.inventory-table-container {
  background: white; border-radius: 16px; overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #f1f5f9;
}

.inventory-table { width: 100%; border-collapse: collapse; }
.inventory-table th {
  background: #f8fafc; text-align: left; padding: 16px;
  color: #64748b; font-size: 13px; text-transform: uppercase; border-bottom: 2px solid #f1f5f9;
}
.inventory-table td { padding: 16px; border-bottom: 1px solid #f1f5f9; }

.name-cell { display: flex; flex-direction: column; }
.name-cell span { font-size: 12px; color: #94a3b8; }

.description-cell {
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  max-width: 500px;
}

.price-cell {
  font-weight: 700;
  color: #137fec;
  white-space: nowrap;
}

.location-tag {
  background: #eff6ff; color: #137fec; padding: 4px 10px; border-radius: 6px;
  font-size: 12px; font-weight: 700;
}

.stock-value { font-weight: 700; }
.stock-value.danger { color: #ef4444; }

.progress-container { width: 100px; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.progress-bar { height: 100%; border-radius: 4px; transition: width 0.5s ease; }

.no-data { text-align: center; padding: 40px; color: #94a3b8; font-style: italic; }

.spinner {
  width: 40px; height: 40px; border: 4px solid #f3f3f3;
  border-top: 4px solid #137fec; border-radius: 50%;
  margin: 0 auto 16px; animation: spin 1s linear infinite;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .controls-container { flex-direction: column; align-items: stretch; }
  .admin-stats-grid { grid-template-columns: 1fr 1fr; }
}
</style>
