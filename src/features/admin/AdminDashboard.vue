<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()

const centerOptions = [
  'Tất cả', 'VaxCenter Quận 1', 'VaxCenter Quận 3', 'VaxCenter Quận 7', 'VaxCenter Bình Thạnh', 'VaxCenter Thủ Đức'
]

// Mock Data for Admin
const staffList = ref([
  { id: 1, name: 'Bác sĩ Minh', email: 'doctor.minh@vaxcenter.vn', location: 'VaxCenter Quận 1', role: 'Staff', age: 38, gender: 'Nam', phone: '0912345678' },
  { id: 2, name: 'Điều dưỡng Hoa', email: 'nurse.hoa@vaxcenter.vn', location: 'VaxCenter Quận 7', role: 'Staff', age: 29, gender: 'Nữ', phone: '0987654321' },
  { id: 3, name: 'Bác sĩ Tuấn', email: 'doctor.tuan@vaxcenter.vn', location: 'VaxCenter Thủ Đức', role: 'Staff', age: 45, gender: 'Nam', phone: '0900111222' },
  { id: 4, name: 'Bác sĩ Lan', email: 'doctor.lan@vaxcenter.vn', location: 'VaxCenter Quận 1', role: 'Staff', age: 32, gender: 'Nữ', phone: '0911223344' }
])

const customerList = ref([
  { id: 101, name: 'Nguyễn Văn A', email: 'customer.a@gmail.com', phone: '0988777666', age: 25, gender: 'Nam', address: 'Quận 3, TP.HCM' },
  { id: 102, name: 'Trần Thị B', email: 'customer.b@gmail.com', phone: '0901234567', age: 22, gender: 'Nữ', address: 'Quận 1, TP.HCM' },
  { id: 103, name: 'Lê Văn C', email: 'customer.c@gmail.com', phone: '0912345678', age: 35, gender: 'Nam', address: 'Quận 7, TP.HCM' }
])

const allAppointments = ref([
  { id: 1, patient: 'Trần Thị B', vaccine: 'Vaccine HPV', location: 'VaxCenter Quận 1', date: '2026-03-04', time: 'Sáng', status: 'Đang chờ' },
  { id: 2, patient: 'Lê Văn C', vaccine: 'Vaccine Cúm', location: 'VaxCenter Quận 7', date: '2026-03-04', time: 'Sáng', status: 'Đã xác nhận' },
  { id: 3, patient: 'Nguyễn Văn A', vaccine: 'Vaccine 6 trong 1', location: 'VaxCenter Quận 1', date: '2026-03-05', time: 'Chiều', status: 'Đang chờ' }
])

// Tabs Logic
const activeTab = ref('overview')

// Staff Filtering
const staffFilterLocation = ref('Tất cả')
const filteredStaffList = computed(() => {
  if (staffFilterLocation.value === 'Tất cả') return staffList.value
  return staffList.value.filter(s => s.location === staffFilterLocation.value)
})

// Staff Management Logic
const showStaffModal = ref(false)
const isEditing = ref(false)
const currentStaff = ref({
  id: null,
  name: '',
  email: '',
  location: 'VaxCenter Quận 1',
  role: 'Staff',
  age: '',
  gender: 'Nam',
  phone: ''
})

const openAddStaff = () => {
  isEditing.value = false
  currentStaff.value = { id: null, name: '', email: '', location: 'VaxCenter Quận 1', role: 'Staff', age: '', gender: 'Nam', phone: '' }
  showStaffModal.value = true
}

const openEditStaff = (staff) => {
  isEditing.value = true
  currentStaff.value = { ...staff }
  showStaffModal.value = true
}

const saveStaff = () => {
  if (!currentStaff.value.name || !currentStaff.value.email) {
    alert('Vui lòng điền tên và email!')
    return
  }
  if (isEditing.value) {
    const index = staffList.value.findIndex(s => s.id === currentStaff.value.id)
    if (index !== -1) staffList.value[index] = { ...currentStaff.value }
  } else {
    const newId = staffList.value.length > 0 ? Math.max(...staffList.value.map(s => s.id)) + 1 : 1
    staffList.value.push({ ...currentStaff.value, id: newId })
  }
  showStaffModal.value = false
  alert('Đã cập nhật danh sách nhân viên!')
}

const deleteStaff = (id) => {
  if (confirm('Bạn có chắc chắn muốn xóa nhân viên này?')) {
    staffList.value = staffList.value.filter(s => s.id !== id)
  }
}
</script>

<template>
  <div class="admin-dashboard">
    <header class="admin-header">
      <div class="header-title">
        <h1>Bảng Quản Trị Hệ Thống</h1>
        <p>Quản lý toàn bộ cơ sở dữ liệu VaxCenter</p>
      </div>
      <div class="header-stats">
        <div class="stat-box">
          <span class="stat-label">Tổng Nhân viên</span>
          <span class="stat-num">{{ staffList.length }}</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Tổng Khách hàng</span>
          <span class="stat-num">{{ customerList.length }}</span>
        </div>
      </div>
    </header>

    <div class="admin-tabs">
      <button @click="activeTab = 'overview'" :class="{active: activeTab === 'overview'}">🏠 Tổng quan</button>
      <button @click="activeTab = 'staff'" :class="{active: activeTab === 'staff'}">👨‍⚕️ Nhân viên</button>
      <button @click="activeTab = 'customers'" :class="{active: activeTab === 'customers'}">👥 Khách hàng</button>
      <button @click="activeTab = 'appointments'" :class="{active: activeTab === 'appointments'}">📅 Lịch hẹn</button>
    </div>

    <div class="admin-content">
      <!-- 1. OVERVIEW -->
      <section v-if="activeTab === 'overview'" class="tab-section">
        <div class="welcome-card">
          <h3>Chào Admin, {{ authStore.user?.name }}</h3>
          <p>Hệ thống hiện đang hoạt động ổn định trên toàn mạng lưới.</p>
        </div>
        <div class="inventory-preview">
          <h3>Thống kê Kho Vaccine</h3>
          <p>Theo dõi tình trạng cung ứng tại các cơ sở.</p>
          <router-link to="/products" class="btn-link">Xem chi tiết kho vaccine →</router-link>
        </div>
      </section>

      <!-- 2. STAFF MANAGEMENT -->
      <section v-if="activeTab === 'staff'" class="tab-section">
        <div class="section-header">
          <div class="header-left">
            <h3>Quản lý Nhân viên</h3>
            <div class="filter-box">
              <label>Cơ sở:</label>
              <select v-model="staffFilterLocation" class="admin-select">
                <option v-for="opt in centerOptions" :key="opt" :value="opt">{{ opt }}</option>
              </select>
            </div>
          </div>
          <button @click="openAddStaff" class="btn-primary">+ Thêm nhân viên</button>
        </div>
        
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Họ tên</th>
                <th>Cơ sở làm việc</th>
                <th>Email & SĐT</th>
                <th>Thông tin</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in filteredStaffList" :key="staff.id">
                <td><strong>{{ staff.name }}</strong></td>
                <td><span class="location-badge">{{ staff.location }}</span></td>
                <td>
                  <div>{{ staff.email }}</div>
                  <div class="small-text">{{ staff.phone }}</div>
                </td>
                <td>{{ staff.age }} tuổi - {{ staff.gender }}</td>
                <td>
                  <div class="table-actions">
                    <button @click="openEditStaff(staff)" class="btn-icon edit" title="Sửa">✏️</button>
                    <button @click="deleteStaff(staff.id)" class="btn-icon delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredStaffList.length === 0">
                <td colspan="5" class="no-data">Không tìm thấy nhân viên tại cơ sở này.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 3. CUSTOMER VIEW -->
      <section v-if="activeTab === 'customers'" class="tab-section">
        <h3>Danh sách Khách hàng</h3>
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Họ tên</th>
                <th>Liên hệ</th>
                <th>Thông tin</th>
                <th>Địa chỉ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cus in customerList" :key="cus.id">
                <td><strong>{{ cus.name }}</strong></td>
                <td>
                  <div>{{ cus.email }}</div>
                  <div class="small-text">{{ cus.phone }}</div>
                </td>
                <td>{{ cus.age }} tuổi - {{ cus.gender }}</td>
                <td>{{ cus.address }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 4. ALL APPOINTMENTS -->
      <section v-if="activeTab === 'appointments'" class="tab-section">
        <h3>Lịch hẹn toàn hệ thống</h3>
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Ngày & Giờ</th>
                <th>Cơ sở</th>
                <th>Khách hàng</th>
                <th>Vaccine</th>
                <th>Trạng thái</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in allAppointments" :key="apt.id">
                <td>{{ apt.date }} ({{ apt.time }})</td>
                <td>{{ apt.location }}</td>
                <td>{{ apt.patient }}</td>
                <td>{{ apt.vaccine }}</td>
                <td>
                  <span :class="['status-tag', apt.status === 'Đã xác nhận' ? 'success' : 'warning']">
                    {{ apt.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- Staff Modal -->
    <div v-if="showStaffModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Chỉnh sửa nhân viên' : 'Thêm nhân viên mới' }}</h2>
          <button @click="showStaffModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Họ và tên</label>
              <input v-model="currentStaff.name" type="text" placeholder="Nguyễn Văn A">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="currentStaff.email" type="email" placeholder="staff@vaxcenter.vn">
            </div>
            <div class="form-group">
              <label>Số điện thoại</label>
              <input v-model="currentStaff.phone" type="text">
            </div>
            <div class="form-group">
              <label>Cơ sở làm việc</label>
              <select v-model="currentStaff.location">
                <option v-for="loc in centerOptions.slice(1)" :key="loc" :value="loc">{{ loc }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Tuổi</label>
              <input v-model="currentStaff.age" type="number">
            </div>
            <div class="form-group">
              <label>Giới tính</label>
              <select v-model="currentStaff.gender">
                <option value="Nam">Nam</option>
                <option value="Nữ">Nữ</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showStaffModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="saveStaff" class="btn btn-primary">Lưu thông tin</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 1240px;
  margin: 0 auto;
  padding: 32px 20px;
}

.admin-header {
  background: #1e293b;
  color: white;
  padding: 40px;
  border-radius: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.header-title h1 { font-size: 32px; margin-bottom: 8px; }
.header-title p { opacity: 0.7; font-size: 16px; }

.header-stats { display: flex; gap: 24px; }
.stat-box {
  background: rgba(255,255,255,0.1);
  padding: 20px 32px;
  border-radius: 16px;
  text-align: center;
  min-width: 160px;
  backdrop-filter: blur(10px);
}
.stat-num { display: block; font-size: 28px; font-weight: 800; color: #38bdf8; }
.stat-label { font-size: 13px; opacity: 0.8; font-weight: 600; text-transform: uppercase; }

.admin-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.admin-tabs button {
  padding: 12px 24px;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 700;
  color: #64748b;
  border-radius: 12px;
  transition: all 0.2s;
  font-size: 15px;
}

.admin-tabs button.active {
  background: #137fec;
  color: white;
}

.tab-section {
  background: white;
  padding: 32px;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header-left h3 { font-size: 22px; color: #1e293b; }

.filter-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-box label { font-weight: 700; color: #64748b; font-size: 14px; }

.admin-select {
  padding: 8px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-weight: 600;
  color: #1e293b;
  outline: none;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th {
  text-align: left;
  padding: 16px;
  border-bottom: 2px solid #f1f5f9;
  color: #94a3b8;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.admin-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
}

.location-badge {
  background: #f0f9ff;
  color: #0369a1;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
}

.small-text { font-size: 13px; color: #94a3b8; margin-top: 4px; }

.table-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  font-size: 16px;
  padding: 8px;
  border-radius: 10px;
  transition: all 0.2s;
}

.btn-icon:hover { transform: scale(1.1); }
.btn-icon.edit:hover { background: #eff6ff; border-color: #137fec; }
.btn-icon.delete:hover { background: #fef2f2; border-color: #ef4444; }

.btn-primary {
  background: #137fec;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover { background: #0b68c5; transform: translateY(-2px); }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white; width: 95%; max-width: 650px;
  border-radius: 24px; overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  padding: 24px 32px; background: #f8fafc;
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 { font-size: 20px; color: #1e293b; }

.close-btn {
  background: none; border: none; font-size: 32px; color: #94a3b8; cursor: pointer;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 32px;
}

.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 14px; font-weight: 700; color: #475569; }
.form-group input, .form-group select {
  padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 12px;
  font-size: 15px; outline: none; transition: border-color 0.2s;
}
.form-group input:focus { border-color: #137fec; }

.modal-footer {
  padding: 24px 32px; background: #f8fafc;
  display: flex; justify-content: flex-end; gap: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-secondary {
  background: white; border: 2px solid #e2e8f0; color: #64748b;
  padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer;
}

.status-tag {
  padding: 6px 12px; border-radius: 99px; font-size: 12px; font-weight: 700;
}
.status-tag.success { background: #dcfce7; color: #166534; }
.status-tag.warning { background: #fef9c3; color: #854d0e; }

.no-data { text-align: center; padding: 48px; color: #94a3b8; font-style: italic; }

.btn-link { color: #137fec; text-decoration: none; font-weight: 700; }
</style>
