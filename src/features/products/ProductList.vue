<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../store/auth'

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

// Mock data: Chi tiết tồn kho theo từng cơ sở
const inventoryData = ref([
  { id: 1, name: 'Vắc xin 6 trong 1 (Infanrix Hexa)', manufacturer: 'GSK (Bỉ)', price: '1.015.000 VNĐ', location: 'VaxCenter Quận 1', stock: 45, batch: 'BN-2024-001' },
  { id: 2, name: 'Vắc xin 6 trong 1 (Infanrix Hexa)', manufacturer: 'GSK (Bỉ)', price: '1.015.000 VNĐ', location: 'VaxCenter Quận 7', stock: 20, batch: 'BN-2024-005' },
  { id: 3, name: 'Vắc xin Phế cầu (Synflorix)', manufacturer: 'GSK (Bỉ)', price: '1.045.000 VNĐ', location: 'VaxCenter Quận 1', stock: 12, batch: 'BN-2024-082' },
  { id: 4, name: 'Vắc xin Phế cầu (Synflorix)', manufacturer: 'GSK (Bỉ)', price: '1.045.000 VNĐ', location: 'VaxCenter Quận 3', stock: 55, batch: 'BN-2024-090' },
  { id: 5, name: 'Vắc xin HPV', manufacturer: 'MSD (Mỹ)', price: '1.790.000 VNĐ', location: 'VaxCenter Quận 1', stock: 8, batch: 'BN-2024-112' },
  { id: 6, name: 'Vắc xin HPV', manufacturer: 'MSD (Mỹ)', price: '1.790.000 VNĐ', location: 'VaxCenter Thủ Đức', stock: 30, batch: 'BN-2024-115' },
  { id: 7, name: 'Vắc xin Cúm (Vaxigrip Tetra)', manufacturer: 'Sanofi Pasteur', price: '350.000 VNĐ', location: 'VaxCenter Bình Thạnh', stock: 150, batch: 'BN-2024-044' },
  { id: 8, name: 'Vắc xin Cúm (Vaxigrip Tetra)', manufacturer: 'Sanofi Pasteur', price: '350.000 VNĐ', location: 'VaxCenter Quận 1', stock: 100, batch: 'BN-2024-045' }
])

const fetchInventory = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
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

  // Lọc theo từ khóa tìm kiếm
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(item => 
      item.name.toLowerCase().includes(q) || 
      item.batch.toLowerCase().includes(q)
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
            <th>Số lô</th>
            <th>Tồn kho</th>
            <th>Tình trạng</th>
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
            <td><code>{{ item.batch }}</code></td>
            <td>
              <span :class="['stock-value', item.stock < 20 ? 'danger' : '']">
                {{ item.stock }} liều
              </span>
            </td>
            <td>
              <div class="progress-container">
                <div class="progress-bar" :style="{ width: Math.min(item.stock, 100) + '%', backgroundColor: item.stock < 20 ? '#ef4444' : '#10b981' }"></div>
              </div>
            </td>
          </tr>
          <tr v-if="filteredInventory.length === 0">
            <td colspan="5" class="no-data">Không tìm thấy dữ liệu kho phù hợp.</td>
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
