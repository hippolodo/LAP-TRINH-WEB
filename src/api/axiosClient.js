// Cấu hình Axios cho Vue
import axios from 'axios';

const axiosClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:3000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosClient;
