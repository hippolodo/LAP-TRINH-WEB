<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()
const staffLocation = authStore.user?.workLocation || 'VaxCenter Quận 1'

// Dữ liệu mẫu ban đầu (bao gồm nhiều cơ sở khác nhau)
const todayAppointments = ref([
  { id: 1, patient: 'Trần Thị B', vaccine: 'Vaccine HPV', location: 'VaxCenter Quận 1', date: '2026-03-04', time: 'Sáng (08:30)', status: 'Đang chờ', age: 22, gender: 'Nữ', phone: '0901234567', address: 'Quận 1, TP.HCM' },
  { id: 2, patient: 'Lê Văn C', vaccine: 'Vaccine Cúm', location: 'VaxCenter Quận 7', date: '2026-03-04', time: 'Sáng (09:15)', status: 'Đã xác nhận', age: 35, gender: 'Nam', phone: '0912345678', address: 'Quận 7, TP.HCM' },
  { id: 3, patient: 'Nguyễn Thị D', vaccine: 'Vaccine Phế cầu', location: 'VaxCenter Quận 1', date: '2026-03-04', time: 'Chiều (14:00)', status: 'Đang chờ', age: 5, gender: 'Nữ', phone: '0988888888', address: 'Quận Bình Thạnh, TP.HCM' },
  { id: 4, patient: 'Phạm Văn E', vaccine: 'Vaccine 6 trong 1', location: 'VaxCenter Quận 1', date: '2026-03-04', time: 'Chiều (15:30)', status: 'Đang chờ', age: 1, gender: 'Nam', phone: '0977666555', address: 'Quận 1, TP.HCM' }
])

// Lọc lịch hẹn trùng với cơ sở của Staff
const filteredByLocation = computed(() => {
  return todayAppointments.value.filter(apt => apt.location === staffLocation)
})

// Trạng thái hiển thị rút gọn/tất cả (dựa trên danh sách đã lọc)
const showAllAppointments = ref(false)
const displayedAppointments = computed(() => {
  return showAllAppointments.value ? filteredByLocation.value : filteredByLocation.value.slice(0, 2)
})

const vaccineOptions = [
  { id: 1, name: 'Vaccine 6 trong 1 (Infanrix Hexa)' },
  { id: 2, name: 'Vaccine Phế cầu (Synflorix)' },
  { id: 3, name: 'Vaccine Sởi - Quai bị - Rubella' },
  { id: 4, name: 'Vaccine Thủy đậu (Varivax)' },
  { id: 5, name: 'Vaccine Viêm não Nhật Bản' },
  { id: 6, name: 'Vaccine Cúm (Vaxigrip Tetra)' },
  { id: 7, name: 'Vaccine HPV' }
]

// Modal Chi tiết
const selectedAppointment = ref(null)
const showDetailModal = ref(false)

// Modal Tạo mới
const showCreateModal = ref(false)
const newRecord = ref({
  patient: '',
  age: '',
  gender: 'Nam',
  vaccine: vaccineOptions[0].name,
  center: staffLocation,
  date: new Date().toISOString().split('T')[0],
  shift: 'Sáng'
})

const openDetails = (apt) => {
  selectedAppointment.value = apt
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedAppointment.value = null
}

const openCreateModal = () => {
  newRecord.value = {
    patient: '',
    age: '',
    gender: 'Nam',
    vaccine: vaccineOptions[0].name,
    center: staffLocation,
    date: new Date().toISOString().split('T')[0],
    shift: 'Sáng'
  }
  showCreateModal.value = true
}

const handleCreateRecord = () => {
  if (!newRecord.value.patient || !newRecord.value.age || !newRecord.value.date) {
    alert('Vui lòng nhập đầy đủ thông tin!')
    return
  }

  const newId = todayAppointments.value.length + 1
  const timeStr = newRecord.value.shift === 'Sáng' ? 'Sáng (Linh hoạt)' : 'Chiều (Linh hoạt)'
  
  todayAppointments.value.push({
    id: newId,
    patient: newRecord.value.patient,
    age: parseInt(newRecord.value.age),
    gender: newRecord.value.gender,
    vaccine: newRecord.value.vaccine,
    location: newRecord.value.center,
    date: newRecord.value.date,
    time: timeStr,
    status: 'Đã xác nhận',
    phone: 'Chưa cập nhật',
    address: 'Đăng ký tại quầy'
  })

  alert('Đã tạo phiếu tiêm thành công!')
  showCreateModal.value = false
}

const handleApprove = (id) => {
  const apt = todayAppointments.value.find(a => a.id === id)
  if (apt) {
    apt.status = 'Đã xác nhận'
    alert(`Đã xác nhận lịch hẹn của ${apt.patient}`)
  }
}

const handleReject = (id) => {
  const apt = todayAppointments.value.find(a => a.id === id)
  if (apt) {
    if (confirm(`Bạn có chắc muốn từ chối lịch hẹn của ${apt.patient}?`)) {
      apt.status = 'Đã từ chối'
    }
  }
}

const vaccineInventory = [
  { id: 1, name: 'Vaccine 6 trong 1', stock: 45, unit: 'liều' },
  { id: 2, name: 'Vaccine HPV', stock: 12, unit: 'liều' },
  { id: 3, name: 'Vaccine Cúm', stock: 120, unit: 'liều' }
]
</script>

<template>
  <div class="staff-dashboard">
    <header class="staff-header">
      <div class="header-content">
        <h1>Bảng điều khiển Nhân viên</h1>
        <p>Cơ sở làm việc: <strong>{{ staffLocation }}</strong></p>
        <p>Chào <strong>{{ authStore.user?.name }}</strong>. Chúc bạn một ngày làm việc hiệu quả!</p>
      </div>
      <div class="header-actions">
        <button @click="openCreateModal" class="btn btn-create">+ Tạo phiếu tiêm mới</button>
      </div>
    </header>

    <div class="dashboard-grid">
      <!-- Appointments Section -->
      <section class="section-card appointments-section">
        <div class="section-header">
          <h2>Lịch hẹn tại cơ sở</h2>
          <button 
            v-if="filteredByLocation.length > 2"
            @click="showAllAppointments = !showAllAppointments" 
            class="view-all-btn"
          >
            {{ showAllAppointments ? 'Rút gọn' : 'Xem tất cả' }}
          </button>
        </div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Ngày & Giờ</th>
                <th>Bệnh nhân</th>
                <th>Vaccine</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in displayedAppointments" :key="apt.id">
                <td>
                  <div class="time-cell">
                    <strong>{{ apt.date }}</strong>
                    <span>{{ apt.time }}</span>
                  </div>
                </td>
                <td>
                   <div class="patient-cell">
                     <strong>{{ apt.patient }}</strong>
                     <span>{{ apt.age }} tuổi - {{ apt.gender }}</span>
                   </div>
                </td>
                <td>{{ apt.vaccine }}</td>
                <td>
                  <span :class="['status-tag', 
                    apt.status === 'Đã xác nhận' ? 'success' : 
                    apt.status === 'Đang chờ' ? 'warning' : 
                    apt.status === 'Đã từ chối' ? 'danger' : '']">
                    {{ apt.status }}
                  </span>
                </td>
                <td>
                  <div class="action-group">
                    <template v-if="apt.status === 'Đang chờ'">
                      <button @click="handleApprove(apt.id)" class="btn-action approve" title="Xác nhận">✓</button>
                      <button @click="handleReject(apt.id)" class="btn-action reject" title="Từ chối">✕</button>
                    </template>
                    <button @click="openDetails(apt)" class="btn-text">Chi tiết</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredByLocation.length === 0">
                <td colspan="5" class="no-data">Không có lịch hẹn nào tại cơ sở của bạn trong hôm nay.</td>
              </tr>
            </tbody>
          </table>
          <p v-if="!showAllAppointments && filteredByLocation.length > 2" class="more-info">
            Đang hiển thị 2 trên {{ filteredByLocation.length }} lịch hẹn tại cơ sở này.
          </p>
        </div>
      </section>

      <!-- Inventory Section -->
      <section class="section-card inventory-section">
        <div class="section-header">
          <h2>Kho Vaccine</h2>
          <router-link to="/products" class="view-all">Xem tất cả</router-link>
        </div>
        <div class="inventory-list">
          <div v-for="item in vaccineInventory" :key="item.id" class="inventory-item">
            <div class="item-info">
              <h4>{{ item.name }}</h4>
              <p>Tồn kho: <strong>{{ item.stock }}</strong> {{ item.unit }}</p>
            </div>
            <div class="stock-bar-container">
              <div class="stock-bar" :style="{ width: (item.stock / 150 * 100) + '%', backgroundColor: item.stock < 20 ? '#ef4444' : '#10b981' }"></div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Create Record Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Tạo phiếu tiêm mới</h2>
          <button @click="showCreateModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleCreateRecord" class="create-form">
            <div class="form-section-label">1. Thông tin người tiêm</div>
            <div class="form-row">
              <div class="form-group flex-2">
                <label>Họ tên khách hàng</label>
                <input v-model="newRecord.patient" type="text" placeholder="Nhập họ tên" required>
              </div>
              <div class="form-group">
                <label>Tuổi</label>
                <input v-model="newRecord.age" type="number" placeholder="Tuổi" required>
              </div>
              <div class="form-group">
                <label>Giới tính</label>
                <select v-model="newRecord.gender">
                  <option value="Nam">Nam</option>
                  <option value="Nữ">Nữ</option>
                  <option value="Khác">Khác</option>
                </select>
              </div>
            </div>

            <div class="form-section-label">2. Dịch vụ & Địa điểm</div>
            <div class="form-row">
              <div class="form-group">
                <label>Loại Vaccine</label>
                <select v-model="newRecord.vaccine">
                  <option v-for="opt in vaccineOptions" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Cơ sở tiêm</label>
                <select v-model="newRecord.center" disabled>
                  <option :value="staffLocation">{{ staffLocation }} (Cơ sở của bạn)</option>
                </select>
              </div>
            </div>
            
            <div class="form-section-label">3. Thời gian tiêm</div>
            <div class="form-row">
              <div class="form-group">
                <label>Ngày tiêm</label>
                <input v-model="newRecord.date" type="date" :min="new Date().toISOString().split('T')[0]" required>
              </div>
              <div class="form-group">
                <label>Ca tiêm</label>
                <div class="radio-group">
                  <label class="radio-label">
                    <input type="radio" value="Sáng" v-model="newRecord.shift"> Sáng
                  </label>
                  <label class="radio-label">
                    <input type="radio" value="Chiều" v-model="newRecord.shift"> Chiều
                  </label>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="showCreateModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="handleCreateRecord" class="btn btn-submit-form">Lưu phiếu tiêm</button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailModal" class="modal-overlay" @click.self="closeDetailModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Chi tiết lịch hẹn</h2>
          <button @click="closeDetailModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body" v-if="selectedAppointment">
          <div class="detail-grid">
            <div class="detail-item">
              <label>Họ tên khách hàng:</label>
              <p>{{ selectedAppointment.patient }}</p>
            </div>
            <div class="detail-item">
              <label>Độ tuổi:</label>
              <p>{{ selectedAppointment.age }} tuổi</p>
            </div>
            <div class="detail-item">
              <label>Giới tính:</label>
              <p>{{ selectedAppointment.gender }}</p>
            </div>
            <div class="detail-item">
              <label>Số điện thoại:</label>
              <p>{{ selectedAppointment.phone }}</p>
            </div>
            <div class="detail-item full-width">
              <label>Địa chỉ:</label>
              <p>{{ selectedAppointment.address }}</p>
            </div>
            <div class="detail-item">
              <label>Loại Vaccine:</label>
              <p>{{ selectedAppointment.vaccine }}</p>
            </div>
            <div class="detail-item">
              <label>Cơ sở tiêm:</label>
              <p>{{ selectedAppointment.location }}</p>
            </div>
            <div class="detail-item">
              <label>Ngày tiêm:</label>
              <p>{{ selectedAppointment.date }}</p>
            </div>
            <div class="detail-item">
              <label>Ca tiêm:</label>
              <p>{{ selectedAppointment.time }}</p>
            </div>
            <div class="detail-item">
              <label>Trạng thái:</label>
              <p>
                <span :class="['status-tag', 
                  selectedAppointment.status === 'Đã xác nhận' ? 'success' : 
                  selectedAppointment.status === 'Đang chờ' ? 'warning' : 
                  selectedAppointment.status === 'Đã từ chối' ? 'danger' : '']">
                  {{ selectedAppointment.status }}
                </span>
              </p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeDetailModal" class="btn btn-secondary">Đóng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.staff-dashboard {
  padding: 32px 0;
}

.staff-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  background: linear-gradient(135deg, #137fec 0%, #0b68c5 100%);
  color: white;
  padding: 32px 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(19, 127, 236, 0.2);
}

.staff-header h1 {
  font-size: 28px;
  color: white;
  margin-bottom: 8px;
}

.staff-header p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 4px;
}

.staff-header strong {
  color: white;
}

.btn-create {
  background-color: white;
  color: #137fec;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.view-all-btn {
  background: none;
  border: none;
  color: #137fec;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
}

.view-all-btn:hover {
  text-decoration: underline;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
  font-style: italic;
}

/* Table styles */
.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid #f1f5f9;
  color: #64748b;
  font-weight: 600;
}

.data-table td {
  padding: 16px 12px;
  border-bottom: 1px solid #f1f5f9;
}

.time-cell {
  display: flex;
  flex-direction: column;
}

.time-cell span {
  font-size: 12px;
  color: #64748b;
}

.patient-cell {
  display: flex;
  flex-direction: column;
}

.patient-cell span {
  font-size: 12px;
  color: #64748b;
}

.status-tag {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-tag.success { background: #dcfce7; color: #166534; }
.status-tag.warning { background: #fef9c3; color: #854d0e; }
.status-tag.danger { background: #fee2e2; color: #991b1b; }

.action-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-action {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-action.approve { background-color: #10b981; color: white; }
.btn-action.approve:hover { background-color: #059669; }
.btn-action.reject { background-color: #ef4444; color: white; }
.btn-action.reject:hover { background-color: #dc2626; }

.btn-text {
  background: none;
  border: none;
  color: #137fec;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
}

.btn-text:hover {
  text-decoration: underline;
}

.more-info {
  margin-top: 16px;
  font-size: 13px;
  color: #64748b;
  font-style: italic;
  text-align: center;
}

.btn-submit-form {
  background-color: #137fec;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  width: 95%;
  max-width: 650px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 20px 24px;
  background: #f8fafc;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  font-size: 20px;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
  max-height: 80vh;
  overflow-y: auto;
}

/* Form Styles */
.create-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section-label {
  font-size: 14px;
  font-weight: 700;
  color: #137fec;
  text-transform: uppercase;
  border-bottom: 1px solid #e0f2fe;
  padding-bottom: 8px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.flex-2 { flex: 2; }

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.form-group input, .form-group select {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 15px;
  background-color: #f8fafc;
}

.radio-group {
  display: flex;
  gap: 24px;
  padding: 8px 0;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  cursor: pointer;
}

/* Detail Modal Styles */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.detail-item label {
  display: block;
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.detail-item p {
  font-size: 15px;
  color: #1e293b;
  font-weight: 600;
}

.full-width {
  grid-column: span 2;
}

.modal-footer {
  padding: 16px 24px;
  background: #f8fafc;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #e2e8f0;
}

/* Inventory styles */
.inventory-item {
  margin-bottom: 20px;
}

.inventory-item h4 {
  margin-bottom: 4px;
  font-size: 16px;
}

.inventory-item p {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 8px;
}

.stock-bar-container {
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.stock-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
