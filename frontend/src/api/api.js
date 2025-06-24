import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Match your backend URL

export const uploadFile = async (file, fileData) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_name', fileData.file_name);
  formData.append('file_type', fileData.file_type);
  formData.append('description', fileData.description);

  return axios.post(`${API_BASE_URL}/upload/upload_data`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const createWebSocket = () => {
  return new WebSocket(`ws://localhost:8000/ws`); // Match your backend URL
};