import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post('/auth/token', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const register = async (email: string, username: string, password: string) => {
  const response = await api.post('/auth/register', {
    email,
    username,
    password,
  });
  return response.data;
};

export const getTransactions = async () => {
  const response = await api.get('/transactions');
  return response.data;
};

export const createTransaction = async (data: {
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string;
}) => {
  const response = await api.post('/transactions', data);
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data;
};

export const getBudgets = async () => {
  const response = await api.get('/budgets');
  return response.data;
};

export const createBudget = async (data: {
  category_id: number;
  amount: number;
  period: 'monthly' | 'yearly';
}) => {
  const response = await api.post('/budgets', data);
  return response.data;
};

export const getUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};

export default api; 