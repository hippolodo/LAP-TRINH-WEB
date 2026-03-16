<script setup>
import { ref, reactive } from 'vue'

const formData = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  gender: '',
  dob: '',
  phone: '',
  cccd: '',
  address: ''
})

const handleRegister = () => {
  if (formData.password !== formData.confirmPassword) {
    alert('Mật khẩu xác nhận không khớp!')
    return
  }
  
  console.log('Đăng ký dữ liệu:', formData)
  alert('Gửi yêu cầu đăng ký cho: ' + formData.fullName)
  // TODO: Gọi API đăng ký tại đây
}
</script>

<template>
  <div class="register-container">
    <div class="register-header">
      <h2>Đăng Ký Tài Khoản</h2>
      <p>Tham gia VaxCenter để bảo vệ sức khỏe gia đình bạn</p>
    </div>

    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-row">
        <div class="form-group">
          <label for="fullName">Họ và Tên</label>
          <input 
            type="text" 
            id="fullName" 
            v-model="formData.fullName" 
            placeholder="VD: Nguyễn Văn A" 
            required 
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email" 
            placeholder="example@gmail.com" 
            required 
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            placeholder="••••••••" 
            required 
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Xác nhận mật khẩu</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="formData.confirmPassword" 
            placeholder="••••••••" 
            required 
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="phone">Số điện thoại</label>
          <input 
            type="tel" 
            id="phone" 
            v-model="formData.phone" 
            placeholder="09xx xxx xxx" 
            required 
          />
        </div>
        <div class="form-group">
          <label for="cccd">Số CCCD / Mã định danh</label>
          <input 
            type="text" 
            id="cccd" 
            v-model="formData.cccd" 
            placeholder="Số căn cước công dân" 
            required 
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="dob">Ngày sinh</label>
          <input 
            type="date" 
            id="dob" 
            v-model="formData.dob" 
            required 
          />
        </div>
        <div class="form-group">
          <label>Giới tính</label>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" value="male" v-model="formData.gender" required /> Nam
            </label>
            <label class="radio-label">
              <input type="radio" value="female" v-model="formData.gender" /> Nữ
            </label>
            <label class="radio-label">
              <input type="radio" value="other" v-model="formData.gender" /> Khác
            </label>
          </div>
        </div>
      </div>

      <div class="form-group full-width">
        <label for="address">Địa chỉ thường trú</label>
        <textarea 
          id="address" 
          v-model="formData.address" 
          placeholder="Số nhà, tên đường, phường/xã, quận/huyện, tỉnh/thành phố" 
          rows="3"
          required
        ></textarea>
      </div>

      <button type="submit" class="btn-submit">Tạo tài khoản</button>
      
      <p class="auth-footer">
        Đã có tài khoản? <router-link to="/login">Đăng nhập ngay</router-link>
      </p>
    </form>
  </div>
</template>

<style scoped>
.register-container {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 700px;
  margin: 32px auto;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h2 {
  color: #137fec;
  font-size: 28.8px;
  margin-bottom: 8px;
}

.register-header p {
  color: #64748b;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 24px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.full-width {
  width: 100%;
}

label {
  font-weight: 600;
  font-size: 14.4px;
  color: #334155;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="tel"],
input[type="date"],
textarea {
  padding: 12px 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.2s ease;
  width: 100%;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #137fec;
  box-shadow: 0 0 0 3px rgba(19, 127, 236, 0.1);
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

.radio-label input {
  width: 19.2px;
  height: 19.2px;
  cursor: pointer;
}

.btn-submit {
  background-color: #137fec;
  color: white;
  padding: 16px;
  border: none;
  border-radius: 8px;
  font-size: 17.6px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 16px;
}

.btn-submit:hover {
  background-color: #0b68c5;
}

.auth-footer {
  text-align: center;
  font-size: 15.2px;
  color: #64748b;
  margin-top: 8px;
}

.auth-footer a {
  color: #137fec;
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 640px) {
  .form-row {
    flex-direction: column;
    gap: 20px;
  }
  
  .register-container {
    padding: 24px;
    margin: 16px;
  }
}
</style>
