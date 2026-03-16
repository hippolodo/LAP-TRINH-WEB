<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()

const centerList = ref([
  { id: 1, name: 'VaxCenter Quận 1', address: '123 Nguyễn Huệ, Quận 1, TP.HCM', status: 'Hoạt động' },
  { id: 2, name: 'VaxCenter Quận 3', address: '456 Võ Văn Tần, Quận 3, TP.HCM', status: 'Hoạt động' },
  { id: 3, name: 'VaxCenter Quận 7', address: '789 Nguyễn Văn Linh, Quận 7, TP.HCM', status: 'Hoạt động' },
  { id: 4, name: 'VaxCenter Bình Thạnh', address: '101 Phan Đăng Lưu, Bình Thạnh, TP.HCM', status: 'Tạm nghỉ' },
  { id: 5, name: 'VaxCenter Thủ Đức', address: '202 Võ Văn Ngân, Thủ Đức, TP.HCM', status: 'Hoạt động' }
])

const centerOptions = computed(() => [
  'Tất cả', ...centerList.value.map(c => c.name)
])

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

const vaccinationRecords = ref([
  { id: 'VXR-001', customerName: 'Trần Thị B', vaccineName: 'Vaccine Viêm gan B', brand: 'Engerix-B (Bỉ)', date: '2023-12-10', location: 'VaxCenter Quận 1', provider: 'BS. Nguyễn Thị Mai', batchNumber: 'HBV-129302', doseNumber: 'Mũi 3', reactions: 'Sức khỏe ổn định' },
  { id: 'VXR-002', customerName: 'Lê Văn C', vaccineName: 'Vaccine HPV', brand: 'Gardasil 9 (Mỹ)', date: '2023-11-05', location: 'VaxCenter Quận 1', provider: 'BS. Lê Mạnh Hùng', batchNumber: 'HPV-90211', doseNumber: 'Mũi 1', reactions: 'Sưng nhẹ tại vị trí tiêm' }
])

// Tabs Logic
const activeTab = ref('overview')
const vaxSubTab = ref('appointments')

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
  password: '',
  location: '',
  role: 'Staff',
  age: '',
  gender: 'Nam',
  phone: ''
})

const openAddStaff = () => {
  isEditing.value = false
  currentStaff.value = { id: null, name: '', email: '', password: '', location: centerList.value[0]?.name || '', role: 'Staff', age: '', gender: 'Nam', phone: '' }
  showStaffModal.value = true
}

const openEditStaff = (staff) => {
  isEditing.value = true
  currentStaff.value = { ...staff, password: '' }
  showStaffModal.value = true
}

const saveStaff = () => {
  if (!currentStaff.value.name || !currentStaff.value.email) {
    alert('Vui lòng điền tên và email!')
    return
  }
  if (!isEditing.value && !currentStaff.value.password) {
    alert('Vui lòng điền mật khẩu cho tài khoản mới!')
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

// Vaccination Record Management Logic
const showVaccinationModal = ref(false)
const isEditingVaccination = ref(false)
const currentVaccination = ref({
  id: '',
  customerName: '',
  vaccineName: '',
  brand: '',
  date: '',
  location: '',
  provider: '',
  batchNumber: '',
  doseNumber: 'Mũi 1',
  reactions: 'Sức khỏe ổn định'
})

const openAddVaccination = () => {
  isEditingVaccination.value = false
  const newId = `VXR-${String(vaccinationRecords.value.length + 1).padStart(3, '0')}`
  currentVaccination.value = { 
    id: newId, customerName: '', vaccineName: '', brand: '', 
    date: new Date().toISOString().split('T')[0], 
    location: centerList.value[0]?.name || '', 
    provider: '', batchNumber: '', doseNumber: 'Mũi 1', reactions: 'Sức khỏe ổn định' 
  }
  showVaccinationModal.value = true
}

const openEditVaccination = (vax) => {
  isEditingVaccination.value = true
  currentVaccination.value = { ...vax }
  showVaccinationModal.value = true
}

const saveVaccination = () => {
  if (!currentVaccination.value.customerName || !currentVaccination.value.vaccineName) {
    alert('Vui lòng điền tên khách hàng và tên vaccine!')
    return
  }
  if (isEditingVaccination.value) {
    const index = vaccinationRecords.value.findIndex(v => v.id === currentVaccination.value.id)
    if (index !== -1) vaccinationRecords.value[index] = { ...currentVaccination.value }
  } else {
    vaccinationRecords.value.push({ ...currentVaccination.value })
  }
  showVaccinationModal.value = false
  alert('Đã cập nhật phiếu tiêm chủng!')
}

const deleteVaccination = (id) => {
  if (confirm('Bạn có chắc chắn muốn xóa phiếu tiêm này?')) {
    vaccinationRecords.value = vaccinationRecords.value.filter(v => v.id !== id)
  }
}

// Appointment Management Logic
const showAppointmentModal = ref(false)
const isEditingAppointment = ref(false)
const currentAppointment = ref({
  id: null,
  patient: '',
  vaccine: '',
  location: '',
  date: '',
  time: 'Sáng',
  status: 'Đang chờ'
})

const openAddAppointment = () => {
  isEditingAppointment.value = false
  currentAppointment.value = { 
    id: null, patient: '', vaccine: '', 
    location: centerList.value[0]?.name || '', 
    date: new Date().toISOString().split('T')[0], 
    time: 'Sáng', status: 'Đang chờ' 
  }
  showAppointmentModal.value = true
}

const openEditAppointment = (apt) => {
  isEditingAppointment.value = true
  currentAppointment.value = { ...apt }
  showAppointmentModal.value = true
}

const saveAppointment = () => {
  if (!currentAppointment.value.patient || !currentAppointment.value.vaccine) {
    alert('Vui lòng chọn khách hàng và vaccine!')
    return
  }
  if (isEditingAppointment.value) {
    const index = allAppointments.value.findIndex(a => a.id === currentAppointment.value.id)
    if (index !== -1) allAppointments.value[index] = { ...currentAppointment.value }
  } else {
    const newId = allAppointments.value.length > 0 ? Math.max(...allAppointments.value.map(a => a.id)) + 1 : 1
    allAppointments.value.push({ ...currentAppointment.value, id: newId })
  }
  showAppointmentModal.value = false
  alert('Đã cập nhật lịch hẹn tiêm chủng!')
}

const deleteAppointment = (id) => {
  if (confirm('Bạn có chắc chắn muốn xóa lịch hẹn này?')) {
    allAppointments.value = allAppointments.value.filter(a => a.id !== id)
  }
}

// Customer Management Logic
const showCustomerModal = ref(false)
const isEditingCustomer = ref(false)
const currentCustomer = ref({
  id: null,
  name: '',
  email: '',
  password: '',
  phone: '',
  age: '',
  gender: 'Nam',
  address: ''
})

const openAddCustomer = () => {
  isEditingCustomer.value = false
  currentCustomer.value = { id: null, name: '', email: '', password: '', phone: '', age: '', gender: 'Nam', address: '' }
  showCustomerModal.value = true
}

const openEditCustomer = (cus) => {
  isEditingCustomer.value = true
  currentCustomer.value = { ...cus, password: '' }
  showCustomerModal.value = true
}

const saveCustomer = () => {
  if (!currentCustomer.value.name || !currentCustomer.value.email) {
    alert('Vui lòng điền tên và email!')
    return
  }
  if (!isEditingCustomer.value && !currentCustomer.value.password) {
    alert('Vui lòng điền mật khẩu cho tài khoản mới!')
    return
  }
  if (isEditingCustomer.value) {
    const index = customerList.value.findIndex(c => c.id === currentCustomer.value.id)
    if (index !== -1) customerList.value[index] = { ...currentCustomer.value }
  } else {
    const newId = customerList.value.length > 0 ? Math.max(...customerList.value.map(c => c.id)) + 1 : 101
    customerList.value.push({ ...currentCustomer.value, id: newId })
  }
  showCustomerModal.value = false
  alert('Đã cập nhật danh sách khách hàng!')
}

const deleteCustomer = (id) => {
  if (confirm('Bạn có chắc chắn muốn xóa khách hàng này?')) {
    customerList.value = customerList.value.filter(c => c.id !== id)
  }
}

// Center Management Logic
const showCenterModal = ref(false)
const isEditingCenter = ref(false)
const currentCenter = ref({
  id: null,
  name: '',
  address: '',
  status: 'Hoạt động'
})

const openAddCenter = () => {
  isEditingCenter.value = false
  currentCenter.value = { id: null, name: '', address: '', status: 'Hoạt động' }
  showCenterModal.value = true
}

const openEditCenter = (center) => {
  isEditingCenter.value = true
  currentCenter.value = { ...center }
  showCenterModal.value = true
}

const saveCenter = () => {
  if (!currentCenter.value.name || !currentCenter.value.address) {
    alert('Vui lòng điền tên và địa chỉ cơ sở!')
    return
  }
  if (isEditingCenter.value) {
    const index = centerList.value.findIndex(c => c.id === currentCenter.value.id)
    if (index !== -1) centerList.value[index] = { ...currentCenter.value }
  } else {
    const newId = centerList.value.length > 0 ? Math.max(...centerList.value.map(c => c.id)) + 1 : 1
    centerList.value.push({ ...currentCenter.value, id: newId })
  }
  showCenterModal.value = false
  alert('Đã cập nhật danh sách cơ sở tiêm!')
}

const deleteCenter = (id) => {
  const center = centerList.value.find(c => c.id === id)
  const hasStaff = staffList.value.some(s => s.location === center?.name)
  
  if (hasStaff) {
    alert('Không thể xóa cơ sở này vì vẫn còn nhân viên đang làm việc tại đây!')
    return
  }

  if (confirm('Bạn có chắc chắn muốn xóa cơ sở tiêm này?')) {
    centerList.value = centerList.value.filter(c => c.id !== id)
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
          <span class="stat-label">Cơ sở tiêm</span>
          <span class="stat-num">{{ centerList.length }}</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Nhân viên</span>
          <span class="stat-num">{{ staffList.length }}</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Khách hàng</span>
          <span class="stat-num">{{ customerList.length }}</span>
        </div>
      </div>
    </header>

    <div class="admin-tabs">
      <button @click="activeTab = 'overview'" :class="{active: activeTab === 'overview'}">🏠 Tổng quan</button>
      <button @click="activeTab = 'centers'" :class="{active: activeTab === 'centers'}">🏥 Cơ sở tiêm</button>
      <button @click="activeTab = 'vaccination-mgmt'" :class="{active: activeTab === 'vaccination-mgmt'}">💉 Quản lý Tiêm chủng</button>
      <button @click="activeTab = 'staff'" :class="{active: activeTab === 'staff'}">👨‍⚕️ Nhân viên</button>
      <button @click="activeTab = 'customers'" :class="{active: activeTab === 'customers'}">👥 Khách hàng</button>
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

      <!-- 2. CENTER MANAGEMENT -->
      <section v-if="activeTab === 'centers'" class="tab-section">
        <div class="section-header">
          <div class="header-left">
            <h3>Quản lý Cơ sở tiêm chủng</h3>
            <p class="small-text">Danh sách các trung tâm VaxCenter trên hệ thống</p>
          </div>
          <button @click="openAddCenter" class="btn-primary">+ Thêm cơ sở mới</button>
        </div>

        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Tên cơ sở</th>
                <th>Địa chỉ</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="center in centerList" :key="center.id">
                <td><strong>{{ center.name }}</strong></td>
                <td>{{ center.address }}</td>
                <td>
                  <span :class="['status-tag', center.status === 'Hoạt động' ? 'success' : 'warning']">
                    {{ center.status }}
                  </span>
                </td>
                <td>
                  <div class="table-actions">
                    <button @click="openEditCenter(center)" class="btn-icon edit" title="Sửa">✏️</button>
                    <button @click="deleteCenter(center.id)" class="btn-icon delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 3. VACCINATION & APPOINTMENT MANAGEMENT (MERGED) -->
      <section v-if="activeTab === 'vaccination-mgmt'" class="tab-section">
        <div class="section-header">
          <div class="header-left">
            <h3>Quản lý Tiêm chủng</h3>
            <div class="sub-tab-nav">
              <button @click="vaxSubTab = 'appointments'" :class="{active: vaxSubTab === 'appointments'}">Lịch hẹn</button>
              <button @click="vaxSubTab = 'records'" :class="{active: vaxSubTab === 'records'}">Phiếu tiêm</button>
            </div>
          </div>
          <button v-if="vaxSubTab === 'appointments'" @click="openAddAppointment" class="btn-primary">+ Đặt lịch tiêm mới</button>
          <button v-if="vaxSubTab === 'records'" @click="openAddVaccination" class="btn-primary">+ Lập phiếu tiêm mới</button>
        </div>

        <!-- Sub Tab: Appointments -->
        <div v-if="vaxSubTab === 'appointments'" class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Ngày & Giờ</th>
                <th>Cơ sở</th>
                <th>Khách hàng</th>
                <th>Vaccine</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
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
                <td>
                  <div class="table-actions">
                    <button @click="openEditAppointment(apt)" class="btn-icon edit" title="Sửa">✏️</button>
                    <button @click="deleteAppointment(apt.id)" class="btn-icon delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Sub Tab: Records -->
        <div v-if="vaxSubTab === 'records'" class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Mã phiếu</th>
                <th>Khách hàng</th>
                <th>Vaccine & Mũi</th>
                <th>Ngày tiêm</th>
                <th>Cơ sở & Người thực hiện</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="vax in vaccinationRecords" :key="vax.id">
                <td><span class="id-badge">{{ vax.id }}</span></td>
                <td><strong>{{ vax.customerName }}</strong></td>
                <td>
                  <div>{{ vax.vaccineName }}</div>
                  <div class="small-text">{{ vax.brand }} - {{ vax.doseNumber }}</div>
                </td>
                <td>{{ vax.date }}</td>
                <td>
                  <div>{{ vax.location }}</div>
                  <div class="small-text">{{ vax.provider }}</div>
                </td>
                <td>
                  <div class="table-actions">
                    <button @click="openEditVaccination(vax)" class="btn-icon edit" title="Sửa">✏️</button>
                    <button @click="deleteVaccination(vax.id)" class="btn-icon delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 4. STAFF MANAGEMENT -->
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
        <div class="section-header">
          <div class="header-left">
            <h3>Danh sách Khách hàng</h3>
            <p class="small-text">Quản lý hồ sơ khách hàng trên hệ thống</p>
          </div>
          <button @click="openAddCustomer" class="btn-primary">+ Thêm khách hàng</button>
        </div>
        
        <div class="table-container">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Họ tên</th>
                <th>Liên hệ</th>
                <th>Thông tin</th>
                <th>Địa chỉ</th>
                <th>Thao tác</th>
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
                <td>
                  <div class="table-actions">
                    <button @click="openEditCustomer(cus)" class="btn-icon edit" title="Sửa">✏️</button>
                    <button @click="deleteCustomer(cus.id)" class="btn-icon delete" title="Xóa">🗑️</button>
                  </div>
                </td>
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

    <!-- Appointment Modal -->
    <div v-if="showAppointmentModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditingAppointment ? 'Chỉnh sửa lịch hẹn' : 'Đăng ký lịch tiêm mới' }}</h2>
          <button @click="showAppointmentModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Khách hàng</label>
              <select v-model="currentAppointment.patient">
                <option value="" disabled>-- Chọn khách hàng --</option>
                <option v-for="cus in customerList" :key="cus.id" :value="cus.name">
                  {{ cus.name }} ({{ cus.phone }})
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Vaccine</label>
              <select v-model="currentAppointment.vaccine">
                <option value="" disabled>-- Chọn vaccine --</option>
                <option value="Vaccine HPV">Vaccine HPV</option>
                <option value="Vaccine Cúm">Vaccine Cúm</option>
                <option value="Vaccine 6 trong 1">Vaccine 6 trong 1</option>
                <option value="Vaccine Viêm gan B">Vaccine Viêm gan B</option>
                <option value="Vaccine Phế cầu">Vaccine Phế cầu</option>
              </select>
            </div>
            <div class="form-group">
              <label>Ngày hẹn</label>
              <input v-model="currentAppointment.date" type="date">
            </div>
            <div class="form-group">
              <label>Buổi hẹn</label>
              <select v-model="currentAppointment.time">
                <option value="Sáng">Sáng</option>
                <option value="Chiều">Chiều</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cơ sở tiêm</label>
              <select v-model="currentAppointment.location">
                <option v-for="loc in centerOptions.slice(1)" :key="loc" :value="loc">{{ loc }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Trạng thái</label>
              <select v-model="currentAppointment.status">
                <option value="Đang chờ">Đang chờ</option>
                <option value="Đã xác nhận">Đã xác nhận</option>
                <option value="Đã hủy">Đã hủy</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAppointmentModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="saveAppointment" class="btn btn-primary">Lưu lịch hẹn</button>
        </div>
      </div>
    </div>

    <!-- Vaccination Modal -->
    <div v-if="showVaccinationModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditingVaccination ? 'Chỉnh sửa phiếu tiêm' : 'Lập phiếu tiêm chủng mới' }}</h2>
          <button @click="showVaccinationModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Mã phiếu</label>
              <input v-model="currentVaccination.id" type="text" readonly style="background: #f1f5f9;">
            </div>
            <div class="form-group">
              <label>Khách hàng</label>
              <input v-model="currentVaccination.customerName" type="text" placeholder="Họ tên khách hàng">
            </div>
            <div class="form-group">
              <label>Tên Vaccine</label>
              <input v-model="currentVaccination.vaccineName" type="text" placeholder="Vaccine HPV, Vaccine Cúm...">
            </div>
            <div class="form-group">
              <label>Hãng/Thương hiệu</label>
              <input v-model="currentVaccination.brand" type="text" placeholder="Gardasil 9 (Mỹ)...">
            </div>
            <div class="form-group">
              <label>Ngày tiêm</label>
              <input v-model="currentVaccination.date" type="date">
            </div>
            <div class="form-group">
              <label>Mũi tiêm thứ</label>
              <select v-model="currentVaccination.doseNumber">
                <option value="Mũi 1">Mũi 1</option>
                <option value="Mũi 2">Mũi 2</option>
                <option value="Mũi 3">Mũi 3</option>
                <option value="Mũi nhắc lại">Mũi nhắc lại</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cơ sở thực hiện</label>
              <select v-model="currentVaccination.location">
                <option v-for="loc in centerOptions.slice(1)" :key="loc" :value="loc">{{ loc }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Người thực hiện (BS/ĐD)</label>
              <input v-model="currentVaccination.provider" type="text" placeholder="BS. Nguyễn Văn A">
            </div>
            <div class="form-group">
              <label>Số lô vaccine</label>
              <input v-model="currentVaccination.batchNumber" type="text" placeholder="HBV-129302">
            </div>
            <div class="form-group">
              <label>Phản ứng sau tiêm</label>
              <input v-model="currentVaccination.reactions" type="text" placeholder="Sức khỏe ổn định...">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showVaccinationModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="saveVaccination" class="btn btn-primary">Lưu phiếu tiêm</button>
        </div>
      </div>
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
              <label>Email (Tài khoản)</label>
              <input v-model="currentStaff.email" type="email" placeholder="staff@vaxcenter.vn">
            </div>
            <div class="form-group">
              <label>Mật khẩu</label>
              <input v-model="currentStaff.password" type="password" placeholder="Nhập mật khẩu mới">
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

    <!-- Center Modal -->
    <div v-if="showCenterModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditingCenter ? 'Chỉnh sửa cơ sở tiêm' : 'Thêm cơ sở tiêm mới' }}</h2>
          <button @click="showCenterModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group" style="grid-column: span 2;">
              <label>Tên cơ sở</label>
              <input v-model="currentCenter.name" type="text" placeholder="VaxCenter Quận X">
            </div>
            <div class="form-group" style="grid-column: span 2;">
              <label>Địa chỉ</label>
              <input v-model="currentCenter.address" type="text" placeholder="Số nhà, Tên đường, Phường/Xã, Quận/Huyện, Tỉnh/Thành phố">
            </div>
            <div class="form-group" style="grid-column: span 2;">
              <label>Trạng thái</label>
              <select v-model="currentCenter.status">
                <option value="Hoạt động">Hoạt động</option>
                <option value="Tạm nghỉ">Tạm nghỉ</option>
                <option value="Đóng cửa">Đóng cửa</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCenterModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="saveCenter" class="btn btn-primary">Lưu cơ sở</button>
        </div>
      </div>
    </div>

    <!-- Customer Modal -->
    <div v-if="showCustomerModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditingCustomer ? 'Chỉnh sửa thông tin khách hàng' : 'Thêm khách hàng mới' }}</h2>
          <button @click="showCustomerModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Họ và tên</label>
              <input v-model="currentCustomer.name" type="text" placeholder="Nguyễn Văn A">
            </div>
            <div class="form-group">
              <label>Email (Tài khoản)</label>
              <input v-model="currentCustomer.email" type="email" placeholder="customer@gmail.com">
            </div>
            <div class="form-group">
              <label>Mật khẩu</label>
              <input v-model="currentCustomer.password" type="password" placeholder="Nhập mật khẩu mới">
            </div>
            <div class="form-group">
              <label>Số điện thoại</label>
              <input v-model="currentCustomer.phone" type="text">
            </div>
            <div class="form-group">
              <label>Tuổi</label>
              <input v-model="currentCustomer.age" type="number">
            </div>
            <div class="form-group">
              <label>Giới tính</label>
              <select v-model="currentCustomer.gender">
                <option value="Nam">Nam</option>
                <option value="Nữ">Nữ</option>
              </select>
            </div>
            <div class="form-group">
              <label>Địa chỉ</label>
              <input v-model="currentCustomer.address" type="text">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCustomerModal = false" class="btn btn-secondary">Hủy</button>
          <button @click="saveCustomer" class="btn btn-primary">Lưu thông tin</button>
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

.sub-tab-nav {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.sub-tab-nav button {
  background: none;
  border: none;
  padding: 4px 0;
  font-weight: 700;
  color: #94a3b8;
  cursor: pointer;
  font-size: 14px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.sub-tab-nav button.active {
  color: #137fec;
  border-bottom-color: #137fec;
}

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

.id-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 6px;
  font-family: monospace;
  font-weight: 700;
  font-size: 13px;
}

.no-data { text-align: center; padding: 48px; color: #94a3b8; font-style: italic; }

.btn-link { color: #137fec; text-decoration: none; font-weight: 700; }
</style>
