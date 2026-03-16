<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()
const isStaff = computed(() => authStore.user?.role === 'staff')
const isAdmin = computed(() => authStore.user?.role === 'admin')

// Mock data for appointments
const appointments = ref([
  { 
    id: 'VC82931', 
    customerName: 'Nguyễn Văn A',
    vaccine: 'Vaccine Cúm Tứ giá (Hà Lan)', 
    location: 'VaxCenter Quận 1', 
    date: '2024-03-20', 
    session: 'Sáng (07:30 - 11:30)',
    status: 'confirmed',
    statusLabel: 'Đã xác nhận',
    confirmedBy: 'BS. Lê Mạnh Hùng',
    createdAt: '2024-03-01',
    postVaccinationNotes: ''
  },
  { 
    id: 'VC10294', 
    customerName: 'Trần Thị B',
    vaccine: 'Vaccine Phế cầu (Bỉ)', 
    location: 'VaxCenter Quận 7', 
    date: '2024-04-15', 
    session: 'Chiều (13:30 - 17:30)',
    status: 'pending',
    statusLabel: 'Chờ xác nhận',
    createdAt: '2024-03-03',
    postVaccinationNotes: ''
  },
  { 
    id: 'VC09123', 
    customerName: 'Lê Văn C',
    vaccine: 'Vaccine HPV (Mỹ)', 
    location: 'VaxCenter Quận 1', 
    date: '2024-02-10', 
    session: 'Sáng (07:30 - 11:30)',
    status: 'completed',
    statusLabel: 'Đã hoàn thành',
    confirmedBy: 'BS. Đặng Thu Thảo',
    createdAt: '2024-01-20',
    postVaccinationNotes: 'Sức khỏe ổn định, không có phản ứng bất thường sau 30 phút theo dõi.'
  }
])

const selectedAppointment = ref(null)
const showModal = ref(false)
const editStatus = ref('')
const postNotes = ref('')

const openDetails = (apt) => {
  selectedAppointment.value = apt
  editStatus.value = apt.status
  postNotes.value = apt.postVaccinationNotes || ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedAppointment.value = null
}

const updateStatus = () => {
  if (!selectedAppointment.value) return
  
  const index = appointments.value.findIndex(a => a.id === selectedAppointment.value.id)
  if (index !== -1) {
    const newStatus = editStatus.value
    let label = ''
    switch(newStatus) {
      case 'pending': label = 'Chờ xác nhận'; break;
      case 'confirmed': label = 'Đã xác nhận'; break;
      case 'completed': label = 'Đã hoàn thành'; break;
      case 'cancelled': label = 'Đã hủy'; break;
    }
    
    appointments.value[index] = {
      ...appointments.value[index],
      status: newStatus,
      statusLabel: label,
      postVaccinationNotes: postNotes.value,
      confirmedBy: (newStatus === 'completed' || newStatus === 'confirmed') ? (appointments.value[index].confirmedBy || authStore.user?.name || 'Nhân viên hệ thống') : appointments.value[index].confirmedBy
    }
    alert('Cập nhật trạng thái thành công!')
    closeModal()
  }
}

const getStatusClass = (status) => {
  switch (status) {
    case 'pending': return 'status-pending'
    case 'confirmed': return 'status-confirmed'
    case 'completed': return 'status-completed'
    case 'cancelled': return 'status-cancelled'
    default: return ''
  }
}
</script>

<template>
  <div class="appointments-container">
    <div class="page-header">
      <h2>Danh sách Lịch hẹn</h2>
      <p>Theo dõi trạng thái và quản lý các lịch tiêm chủng của bạn</p>
    </div>

    <div class="appointments-list" v-if="appointments.length > 0">
      <div v-for="apt in appointments" :key="apt.id" class="appointment-card">
        <div class="card-header">
          <span class="appointment-id">Mã lịch hẹn: <strong>{{ apt.id }}</strong></span>
          <span :class="['status-badge', getStatusClass(apt.status)]">
            {{ apt.statusLabel }}
          </span>
        </div>
        
        <div class="card-body">
          <div class="info-group">
            <span class="info-label">Vaccine</span>
            <span class="info-value">{{ apt.vaccine }}</span>
          </div>
          
          <div class="info-group">
            <span class="info-label">Địa điểm</span>
            <span class="info-value">{{ apt.location }}</span>
          </div>

          <div class="info-row">
            <div class="info-group">
              <span class="info-label">Ngày tiêm</span>
              <span class="info-value">{{ apt.date }}</span>
            </div>
            <div class="info-group">
              <span class="info-label">Buổi tiêm</span>
              <span class="info-value">{{ apt.session }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <span class="created-at">Ngày đặt: {{ apt.createdAt }}</span>
          <div class="actions">
            <button v-if="apt.status === 'pending'" class="btn-cancel">Hủy lịch</button>
            <button @click="openDetails(apt)" class="btn-detail">Xem chi tiết</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Chi Tiết Lịch Hẹn</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        
        <div class="modal-body" v-if="selectedAppointment">
          <div class="detail-section status-section">
             <span :class="['status-badge', getStatusClass(selectedAppointment.status)]">
              {{ selectedAppointment.statusLabel }}
            </span>
            <p class="appointment-id-large">Mã số: {{ selectedAppointment.id }}</p>
            <p v-if="isStaff" class="customer-name-tag">Khách hàng: <strong>{{ selectedAppointment.customerName }}</strong></p>
          </div>

          <div class="detail-grid">
            <!-- Staff Update Form -->
            <div v-if="isStaff" class="staff-update-form">
              <div class="form-group">
                <label>Cập nhật trạng thái</label>
                <select v-model="editStatus" class="status-select">
                  <option value="pending">Chờ xác nhận</option>
                  <option value="confirmed">Đã xác nhận</option>
                  <option value="completed">Đã hoàn thành</option>
                  <option value="cancelled">Đã hủy</option>
                </select>
              </div>
              <div class="form-group">
                <label>Mô tả sau tiêm (Dành cho khách hàng)</label>
                <textarea 
                  v-model="postNotes" 
                  placeholder="Nhập tình trạng sức khỏe sau tiêm, dặn dò..."
                  class="notes-textarea"
                ></textarea>
              </div>
            </div>

            <div class="detail-item">
              <label>Vaccine</label>
              <p>{{ selectedAppointment.vaccine }}</p>
            </div>
            
            <div v-if="selectedAppointment.postVaccinationNotes && !isStaff" class="detail-item post-notes-box">
              <label>📌 Mô tả sau tiêm</label>
              <p class="post-notes-content">{{ selectedAppointment.postVaccinationNotes }}</p>
            </div>

            <div class="detail-item">
              <label>Địa điểm tiêm</label>
              <p>{{ selectedAppointment.location }}</p>
            </div>
            <div class="detail-item">
              <label>Thời gian</label>
              <p>{{ selectedAppointment.date }} | {{ selectedAppointment.session }}</p>
            </div>
            
            <!-- Doctor Info: Only show if confirmed or completed -->
            <div class="detail-item doctor-info" v-if="selectedAppointment.confirmedBy">
              <label>Bác sĩ/Nhân viên xác nhận</label>
              <div class="doctor-badge">
                <span class="doctor-icon">👨‍⚕️</span>
                <p class="doctor-name">{{ selectedAppointment.confirmedBy }}</p>
              </div>
            </div>

            <div class="detail-item" v-if="selectedAppointment.status === 'pending' && !isStaff">
              <label>Ghi chú</label>
              <p class="note">Lịch hẹn của bạn đang được hệ thống xử lý. Vui lòng đợi thông báo xác nhận từ bác sĩ chuyên môn.</p>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button v-if="isStaff" class="btn-save" @click="updateStatus">Lưu thay đổi</button>
          <button class="btn-primary" @click="closeModal">Đóng</button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">📅</div>
      <h3>Bạn chưa có lịch hẹn nào</h3>
      <p>Hãy đặt lịch tiêm chủng để bảo vệ sức khỏe cho mình và người thân.</p>
      <router-link to="/appointments" class="btn-book-now">Đặt lịch ngay</router-link>
    </div>
  </div>
</template>

<style scoped>
.appointments-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h2 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.page-header p {
  color: #64748b;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.appointment-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: transform 0.2s;
}

.appointment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 16px 24px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.appointment-id {
  color: #475569;
  font-size: 14px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-confirmed {
  background: #dcfce7;
  color: #166534;
}

.status-completed {
  background: #e0f2fe;
  color: #075985;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.card-body {
  padding: 24px;
}

.info-group {
  margin-bottom: 16px;
}

.info-group:last-child {
  margin-bottom: 0;
}

.info-label {
  display: block;
  font-size: 12px;
  text-transform: uppercase;
  color: #94a3b8;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.info-value {
  display: block;
  font-size: 16px;
  color: #1e293b;
  font-weight: 500;
}

.info-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.card-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.created-at {
  font-size: 13px;
  color: #94a3b8;
}

.actions {
  display: flex;
  gap: 12px;
}

.btn-detail {
  padding: 8px 16px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-detail:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.btn-cancel {
  padding: 8px 16px;
  background: white;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #dc2626;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #fef2f2;
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
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 20px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 20px;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #94a3b8;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
}

.status-section {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f1f5f9;
}

.appointment-id-large {
  margin-top: 12px;
  font-weight: 700;
  color: #475569;
  font-size: 18px;
}

.customer-name-tag {
  margin-top: 8px;
  color: #137fec;
}

.staff-update-form {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.status-select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  font-weight: 600;
}

.notes-textarea {
  width: 100%;
  height: 100px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  resize: vertical;
  font-family: inherit;
}

.post-notes-box {
  background: #fffbeb;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #fef3c7;
}

.post-notes-content {
  color: #92400e !important;
  font-weight: 500;
}

.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-item label {
  display: block;
  font-size: 12px;
  text-transform: uppercase;
  color: #94a3b8;
  font-weight: 700;
  margin-bottom: 6px;
}

.detail-item p {
  font-size: 16px;
  color: #1e293b;
  font-weight: 500;
}

.doctor-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f0f7ff;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #137fec;
  margin-top: 4px;
}

.doctor-icon {
  font-size: 24px;
}

.doctor-name {
  color: #137fec !important;
  font-weight: 700 !important;
}

.note {
  font-style: italic;
  color: #64748b !important;
  font-size: 14px !important;
  line-height: 1.5;
}

.modal-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  text-align: right;
}

.btn-primary {
  padding: 10px 24px;
  background: #137fec;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-save {
  padding: 10px 24px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-right: 12px;
}

.btn-save:hover {
  background: #059669;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 24px;
  margin-bottom: 12px;
  color: #1e293b;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 32px;
}

.btn-book-now {
  display: inline-block;
  padding: 14px 32px;
  background: #137fec;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  transition: background 0.3s;
}

.btn-book-now:hover {
  background: #0b68c5;
}

@media (max-width: 640px) {
  .info-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .card-footer {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  .actions {
    width: 100%;
  }
  .actions button {
    flex: 1;
  }
}
</style>
