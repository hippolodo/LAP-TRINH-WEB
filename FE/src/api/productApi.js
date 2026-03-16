import axiosClient from './axiosClient';

const productApi = {
  getAll: () => {
    return axiosClient.get('/vaccines');
  },
  getById: (id) => {
    return axiosClient.get(`/vaccines/${id}`);
  },
  getInventory: () => {
    return axiosClient.get('/inventory');
  },
};

export default productApi;
