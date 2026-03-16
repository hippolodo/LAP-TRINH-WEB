<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const authStore = useAuthStore()

// Mock Data
const vaccines = [
  { id: 1, name: 'Vaccine 6 trong 1 (Infanrix Hexa)', price: 1015000 },
  { id: 2, name: 'Vaccine Phế cầu (Synflorix)', price: 1045000 },
  { id: 3, name: 'Vaccine Sởi - Quai bị - Rubella', price: 300000 },
  { id: 4, name: 'Vaccine Thủy đậu', price: 915000 },
  { id: 5, name: 'Vaccine Viêm não Nhật Bản', price: 670000 },
  { id: 6, name: 'Vaccine Cúm (Vaxigrip Tetra)', price: 350000 },
  { id: 7, name: 'Vaccine HPV', price: 1790000 }
]

const locations = [
  { id: 1, name: 'VaxCenter Quận 1', address: '123 Nguyễn Huệ, Quận 1' },
  { id: 2, name: 'VaxCenter Quận 3', address: '789 Võ Văn Ngân, Quận 3' },
  { id: 3, name: 'VaxCenter Quận 7', address: '456 Nguyễn Văn Linh, Quận 7' },
  { id: 4, name: 'VaxCenter Bình Thạnh', address: '159 Xô Viết Nghệ Tĩnh, Bình Thạnh' },
  { id: 5, name: 'VaxCenter Thủ Đức', address: '789 Võ Văn Ngân, Thủ Đức' }
]

// Form State
const bookingForm = reactive({
  patientName: authStore.user?.name || '',
  age: '',
  gender: 'Nam',
  vaccineId: null,
  locationId: null,
  date: '',
  session: '' // 'morning' or 'afternoon'
})

// Slot Management Logic
const getMockSlots = (locationId, date) => {
  return {
    morning: { occupied: Math.floor(Math.random() * 51), label: 'Sáng (07:30 - 11:30)' },
    afternoon: { occupied: Math.floor(Math.random() * 51), label: 'Chiều (13:30 - 17:30)' }
  }
}

const currentSlots = ref(null)

const handleDateChange = () => {
  if (bookingForm.locationId && bookingForm.date) {
    currentSlots.value = getMockSlots(bookingForm.locationId, bookingForm.date)
  }
}

const handleLocationChange = () => {
  if (bookingForm.locationId && bookingForm.date) {
    currentSlots.value = getMockSlots(bookingForm.locationId, bookingForm.date)
  }
}

const isSubmitting = ref(false)
const submitBooking = () => {
  if (!bookingForm.patientName || !bookingForm.age || !bookingForm.vaccineId || !bookingForm.locationId || !bookingForm.date || !bookingForm.session) {
    alert('Vui lòng điền đầy đủ thông tin!')
    return
  }
  
  isSubmitting.value = true
  setTimeout(() => {
    isSubmitting.value = false
    alert('Đặt lịch thành công! Mã số lịch hẹn của bạn là: VC' + Math.floor(Math.random() * 100000))
    router.push('/')
  }, 1500)
}

const selectedVaccine = computed(() => vaccines.find(v => v.id === bookingForm.vaccineId))
const selectedLocation = computed(() => locations.find(l => l.id === bookingForm.locationId))

</script>

<template>
  <div class="booking-container">
    <div class="booking-card">
      <header class="booking-header">
        <h2>Đặt Lịch Tiêm Chủng</h2>
        <p>Hệ thống đăng ký tiêm chủng trực tuyến VaxCenter</p>
      </header>

      <form @submit.prevent="submitBooking" class="booking-form">
        <!-- 1. Thông tin người tiêm -->
        <div class="form-section">
          <label><span class="step-num">1</span> Thông tin người tiêm</label>
          <div class="form-grid">
            <div class="input-group">
              <input type="text" v-model="bookingForm.patientName" placeholder="Họ tên người tiêm" required />
            </div>
            <div class="input-row">
              <input type="number" v-model="bookingForm.age" placeholder="Tuổi" required />
              <select v-model="bookingForm.gender" required>
                <option value="Nam">Nam</option>
                <option value="Nữ">Nữ</option>
                <option value="Khác">Khác</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 2. Chọn Vaccine & Địa điểm -->
        <div class="form-grid">
          <div class="form-section">
            <label><span class="step-num">2</span> Chọn loại Vaccine</label>
            <div class="select-wrapper">
              <select v-model="bookingForm.vaccineId" required>
                <option :value="null" disabled>-- Chọn Vaccine --</option>
                <option v-for="vax in vaccines" :key="vax.id" :value="vax.id">
                  {{ vax.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-section">
            <label><span class="step-num">3</span> Chọn trung tâm</label>
            <div class="select-wrapper">
              <select v-model="bookingForm.locationId" @change="handleLocationChange" required>
                <option :value="null" disabled>-- Chọn trung tâm --</option>
                <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                  {{ loc.name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- 3. Chọn Ngày & Slot -->
        <div class="form-grid">
          <div class="form-section">
            <label><span class="step-num">4</span> Chọn ngày tiêm</label>
            <input 
              type="date" 
              v-model="bookingForm.date" 
              @change="handleDateChange"
              :min="new Date().toISOString().split('T')[0]"
              required
            />
          </div>

          <div class="form-section" v-if="currentSlots">
            <label><span class="step-num">5</span> Chọn buổi tiêm</label>
            <div class="slots-grid">
              <label 
                v-for="(slot, key) in currentSlots" 
                :key="key"
                class="slot-option"
                :class="{ 
                  'full': slot.occupied >= 50,
                  'selected': bookingForm.session === key 
                }"
              >
                <input 
                  type="radio" 
                  v-model="bookingForm.session" 
                  :value="key" 
                  :disabled="slot.occupied >= 50"
                  name="session"
                />
                <div class="slot-content">
                  <span class="slot-label">{{ slot.label }}</span>
                  <span class="slot-status">
                    Trống: {{ 50 - slot.occupied }}/50
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="booking-summary" v-if="selectedVaccine && selectedLocation && bookingForm.date && bookingForm.session">
          <h3>Xác nhận thông tin đặt lịch</h3>
          <div class="summary-details">
            <p><strong>Họ tên:</strong> {{ bookingForm.patientName }} ({{ bookingForm.age }} tuổi - {{ bookingForm.gender }})</p>
            <p><strong>Vaccine:</strong> {{ selectedVaccine.name }}</p>
            <p><strong>Địa điểm:</strong> {{ selectedLocation.name }}</p>
            <p><strong>Thời gian:</strong> {{ bookingForm.date }} ({{ currentSlots[bookingForm.session].label }})</p>
            <p class="total"><strong>Phí dự kiến:</strong> {{ selectedVaccine.price.toLocaleString() }}đ</p>
          </div>
        </div>

        <button type="submit" class="btn-submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Đang xử lý...' : 'Xác nhận Đặt lịch' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.booking-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
}

.booking-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  overflow: hidden;
}

.booking-header {
  background: #137fec;
  color: white;
  padding: 40px;
  text-align: center;
}

.booking-header h2 {
  font-size: 28px;
  margin-bottom: 8px;
}

.booking-header p {
  opacity: 0.9;
}

.booking-form {
  padding: 40px;
}

.form-section {
  margin-bottom: 32px;
}

.form-section label {
  display: block;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-num {
  background: #137fec;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.input-group {
  margin-bottom: 12px;
}

.input-row {
  display: flex;
  gap: 12px;
}

.input-row input {
  flex: 1;
}

.input-row select {
  width: 120px;
}

select, input[type="text"], input[type="number"], input[type="date"] {
  width: 100%;
  padding: 14px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
  background: #f8fafc;
}

select:focus, input:focus {
  border-color: #137fec;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* Slots Grid */
.slots-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.slot-option {
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  background: #f8fafc;
}

.slot-option input {
  position: absolute;
  opacity: 0;
}

.slot-content {
  display: flex;
  flex-direction: column;
}

.slot-label {
  font-weight: 600;
  color: #2c3e50;
}

.slot-status {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
}

.slot-option:hover:not(.full) {
  border-color: #137fec;
  background: #f0f7ff;
}

.slot-option.selected {
  border-color: #137fec;
  background: #137fec;
}

.slot-option.selected .slot-label,
.slot-option.selected .slot-status {
  color: white;
}

.slot-option.full {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f1f5f9;
}

/* Summary */
.booking-summary {
  background: #f0f7ff;
  border: 1px dashed #137fec;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
}

.booking-summary h3 {
  color: #137fec;
  margin-bottom: 16px;
  font-size: 18px;
}

.summary-details p {
  margin-bottom: 8px;
  color: #475569;
}

.total {
  font-size: 18px;
  color: #2c3e50;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #cbd5e1;
}

.btn-submit {
  width: 100%;
  padding: 16px;
  background: #137fec;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-submit:hover:not(:disabled) {
  background: #0b68c5;
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
