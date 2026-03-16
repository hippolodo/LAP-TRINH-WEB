<script setup>
import { ref } from 'vue'

const vaccinationHistory = ref([
  {
    id: 'VXR-001',
    vaccineName: 'Vaccine Viêm gan B',
    brand: 'Engerix-B (Bỉ)',
    date: '10/12/2023',
    location: 'VaxCenter Quận 1',
    provider: 'BS. Nguyễn Thị Mai',
    batchNumber: 'HBV-129302',
    doseNumber: 'Mũi 3',
    reactions: 'Sức khỏe ổn định, không có phản ứng bất thường sau 30 phút theo dõi.',
    type: 'completed'
  },
  {
    id: 'VXR-002',
    vaccineName: 'Vaccine HPV',
    brand: 'Gardasil 9 (Mỹ)',
    date: '05/11/2023',
    location: 'VaxCenter Quận 1',
    provider: 'BS. Lê Mạnh Hùng',
    batchNumber: 'HPV-90211',
    doseNumber: 'Mũi 1',
    reactions: 'Sưng nhẹ và hơi đỏ tại vị trí tiêm, tự hết sau khoảng 24 giờ.',
    type: 'completed'
  },
  {
    id: 'VXR-003',
    vaccineName: 'Vaccine Cúm Mùa',
    brand: 'Influvac Tetra (Hà Lan)',
    date: '15/10/2023',
    location: 'VaxCenter Quận 7',
    provider: 'ĐD. Trần Văn Bình',
    batchNumber: 'FLU-2023-X',
    doseNumber: 'Mũi nhắc lại',
    reactions: 'Đau mỏi cơ nhẹ toàn thân, không sốt, sinh hoạt bình thường.',
    type: 'completed'
  }
])
</script>

<template>
  <div class="vaccination-timeline-container">
    <div class="header-section">
      <h3>Sổ Tiêm Chủng Điện Tử</h3>
      <p>Lịch sử các mũi tiêm đã thực hiện</p>
    </div>

    <!-- Summary Row -->
    <div class="summary-row">
      <div class="summary-item">
        <span class="s-label">Tổng mũi tiêm</span>
        <span class="s-value">03</span>
      </div>
      <div class="summary-item">
        <span class="s-label">Mũi tiếp theo</span>
        <span class="s-value next">05/2024</span>
      </div>
    </div>

    <!-- Timeline List -->
    <div class="timeline">
      <div v-for="(record, index) in vaccinationHistory" :key="record.id" class="timeline-item">
        <!-- Dot and Line -->
        <div class="timeline-marker">
          <div class="dot"></div>
          <div v-if="index !== vaccinationHistory.length - 1" class="line"></div>
        </div>

        <!-- Content Card -->
        <div class="timeline-content">
          <div class="record-card">
            <div class="card-main">
              <div class="date-info">
                <span class="day">{{ record.date.split('/')[0] }}</span>
                <span class="month-year">tháng {{ record.date.split('/')[1] }}, {{ record.date.split('/')[2] }}</span>
              </div>
              
              <div class="vax-details">
                <div class="vax-header">
                  <h4>{{ record.vaccineName }}</h4>
                  <span class="dose-badge">{{ record.doseNumber }}</span>
                </div>
                <p class="brand">{{ record.brand }}</p>
                
                <div class="meta-info">
                  <div class="meta-item">
                    <span class="icon">📍</span> {{ record.location }}
                  </div>
                  <div class="meta-item">
                    <span class="icon">👨‍⚕️</span> {{ record.provider }}
                  </div>
                  <div class="meta-item">
                    <span class="icon">📦</span> Lô: {{ record.batchNumber }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Reaction Section: Highlighted for visibility -->
            <div class="card-reaction">
              <div class="reaction-label">
                <span class="icon">📝</span> Phản ứng sau tiêm:
              </div>
              <p class="reaction-text">{{ record.reactions }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vaccination-timeline-container {
  max-width: 800px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 32px;
}

.header-section h3 {
  font-size: 26px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.header-section p {
  color: #7f8c8d;
  font-size: 16px;
}

/* Summary Box */
.summary-row {
  display: flex;
  gap: 24px;
  margin-bottom: 40px;
  background: white;
  padding: 20px 32px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid #f0f0f0;
}

.summary-item {
  display: flex;
  flex-direction: column;
}

.s-label {
  font-size: 13px;
  color: #95a5a6;
  font-weight: 600;
  margin-bottom: 4px;
}

.s-value {
  font-size: 20px;
  font-weight: 800;
  color: #2c3e50;
}

.s-value.next {
  color: #137fec;
}

/* Timeline Logic */
.timeline {
  display: flex;
  flex-direction: column;
}

.timeline-item {
  display: flex;
  gap: 20px;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.dot {
  width: 16px;
  height: 16px;
  background: #137fec;
  border-radius: 50%;
  border: 3px solid #e1f0ff;
}

.line {
  width: 2px;
  flex-grow: 1;
  background: #e1f0ff;
  margin: 4px 0;
}

.timeline-content {
  flex-grow: 1;
  padding-bottom: 40px;
}

/* Record Card */
.record-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f0f0f0;
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.record-card:hover {
  box-shadow: 0 8px 16px rgba(0,0,0,0.05);
  border-color: #e1f0ff;
}

.card-main {
  padding: 24px;
  display: flex;
  gap: 24px;
}

.date-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  background: #f8fbff;
  border-radius: 12px;
  padding: 12px;
}

.day {
  font-size: 28px;
  font-weight: 800;
  color: #137fec;
  line-height: 1;
}

.month-year {
  font-size: 11px;
  font-weight: 700;
  color: #7f8c8d;
  text-transform: uppercase;
  margin-top: 4px;
  text-align: center;
}

.vax-details {
  flex-grow: 1;
}

.vax-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px;
}

.vax-header h4 {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
}

.dose-badge {
  background: #e1f0ff;
  color: #137fec;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
}

.brand {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 16px;
}

.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.meta-item {
  font-size: 13px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Reaction Section */
.card-reaction {
  background: #fdfdfd;
  padding: 16px 24px;
  border-top: 1px solid #f9f9f9;
}

.reaction-label {
  font-size: 12px;
  font-weight: 700;
  color: #95a5a6;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.reaction-text {
  font-size: 14px;
  color: #5d6d7e;
  line-height: 1.5;
  font-style: italic;
}

@media (max-width: 600px) {
  .card-main {
    flex-direction: column;
    gap: 16px;
  }
  .date-info {
    flex-direction: row;
    justify-content: flex-start;
    gap: 8px;
    width: 100%;
    padding: 8px 16px;
  }
  .day { font-size: 20px; }
  .month-year { font-size: 14px; margin-top: 0; }
  .vax-header { flex-direction: column; gap: 8px; }
}
</style>
