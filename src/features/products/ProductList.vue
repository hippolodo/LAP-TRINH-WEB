<script setup>
import { ref, computed, onMounted } from 'vue'
import productApi from '../../api/productApi'

const products = ref([])
const searchQuery = ref('')
const loading = ref(true)
const error = ref(null)

const fetchProducts = async () => {
  loading.value = true
  try {
    // Mock data for vaccines (products)
    setTimeout(() => {
      products.value = [
        {
          id: 1,
          name: 'Vắc xin 6 trong 1 (Infanrix Hexa)',
          manufacturer: 'GSK (Bỉ)',
          use: 'Phòng 6 bệnh: Bạch hầu, ho gà, uốn ván, bại liệt, viêm gan B và các bệnh do vi khuẩn Hib.',
          price: '1.015.000 VNĐ'
        },
        {
          id: 2,
          name: 'Vắc xin Phế cầu (Synflorix)',
          manufacturer: 'GSK (Bỉ)',
          use: 'Phòng các bệnh do phế cầu khuẩn như viêm phổi, viêm màng não, viêm tai giữa.',
          price: '1.045.000 VNĐ'
        },
        {
          id: 3,
          name: 'Vắc xin Sởi - Quai bị - Rubella (MMR II)',
          manufacturer: 'MSD (Mỹ)',
          use: 'Phòng 3 bệnh: Sởi, Quai bị, Rubella.',
          price: '300.000 VNĐ'
        },
        {
          id: 4,
          name: 'Vắc xin Thủy đậu (Varivax)',
          manufacturer: 'MSD (Mỹ)',
          use: 'Phòng bệnh Thủy đậu.',
          price: '915.000 VNĐ'
        },
        {
          id: 5,
          name: 'Vắc xin Viêm não Nhật Bản (Imojev)',
          manufacturer: 'Sanofi Pasteur (Pháp)',
          use: 'Phòng bệnh Viêm não Nhật Bản.',
          price: '670.000 VNĐ'
        },
        {
          id: 6,
          name: 'Vắc xin Cúm (Vaxigrip Tetra)',
          manufacturer: 'Sanofi Pasteur (Pháp)',
          use: 'Phòng 4 chủng virus cúm (2 chủng A và 2 chủng B).',
          price: '350.000 VNĐ'
        }
      ]
      loading.value = false
    }, 500)
  } catch (err) {
    error.value = 'Không thể tải danh sách sản phẩm. Vui lòng thử lại sau.'
    loading.value = false
  }
}

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value
  
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(p => 
    p.name.toLowerCase().includes(query) || 
    p.manufacturer.toLowerCase().includes(query) ||
    p.use.toLowerCase().includes(query)
  )
})

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="product-lookup">
    <header class="page-header">
      <h1>Tra cứu Vaccine & Sản phẩm</h1>
      <p>Tìm kiếm thông tin chi tiết về các loại vaccine và sản phẩm y tế</p>
    </header>

    <div class="search-container">
      <div class="search-bar">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Nhập tên vaccine, nhà sản xuất hoặc công dụng..."
          class="search-input"
        >
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Đang tải dữ liệu...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="btn btn-retry">Thử lại</button>
    </div>

    <div v-else>
      <div v-if="filteredProducts.length > 0" class="product-grid">
        <div v-for="product in filteredProducts" :key="product.id" class="product-card">
          <div class="product-header">
            <h3>{{ product.name }}</h3>
            <span class="manufacturer-tag">{{ product.manufacturer }}</span>
          </div>
          <div class="product-body">
            <div class="info-group">
              <label>Công dụng:</label>
              <p>{{ product.use }}</p>
            </div>
            <div class="product-footer">
              <span class="price">{{ product.price }}</span>
              <router-link :to="{ path: '/appointments', query: { productId: product.id } }" class="btn-book">
                Đặt lịch tiêm
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-results">
        <p>Không tìm thấy kết quả nào phù hợp với từ khóa "{{ searchQuery }}"</p>
      </div>
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
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.page-header p {
  color: #64748b;
  font-size: 18px;
}

.search-container {
  margin-bottom: 40px;
  display: flex;
  justify-content: center;
}

.search-bar {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #137fec;
  box-shadow: 0 0 0 4px rgba(19, 127, 236, 0.1);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.product-header {
  padding: 24px;
  background-color: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.product-header h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #1e293b;
  line-height: 1.4;
}

.manufacturer-tag {
  display: inline-block;
  padding: 4px 12px;
  background-color: #e0f2fe;
  color: #0369a1;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}

.product-body {
  padding: 24px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.info-group {
  margin-bottom: 20px;
  flex-grow: 1;
}

.info-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-group p {
  color: #334155;
  line-height: 1.6;
  margin: 0;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
}

.price {
  font-size: 18px;
  font-weight: 700;
  color: #059669;
}

.btn-book {
  background-color: #137fec;
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.btn-book:hover {
  background-color: #0b68c5;
}

.loading-state, .error-state, .no-results {
  text-align: center;
  padding: 80px 0;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #137fec;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-retry {
  margin-top: 16px;
  background-color: #137fec;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 6px;
  cursor: pointer;
}

@media (max-width: 640px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
