import axios from "axios";

// ✅ Create axios instance
const api = axios.create({
  baseURL: import.meta.env.PROD ? "" : (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"),
});

// ✅ Attach token automatically to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ======================
// 🔐 LOGIN FUNCTION
// ======================
export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // ⚠️ FastAPI expects 'username'
  formData.append("password", password);

  const response = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  // ✅ Store token
  localStorage.setItem("token", response.data.access_token);

  return response.data;
};

// ======================
// 👤 GET CURRENT USER
// ======================
export const getMe = async () => {
  const response = await api.get("/auth/me");
  return response;
};

export const getCurrentUser = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

// ======================
// 🏫 DEPARTMENTS
// ======================
export const createDepartment = async (name) => {
  const response = await api.post("/department/", {
    name,
  });
  return response.data;
};

export const listDepartments = async () => {
  const response = await api.get("/department/");
  return response;
};

// ======================
// 👨‍🎓 USERS
// ======================
export const createUser = async (data) => {
  const response = await api.post("/auth/users", data);
  return response.data;
};

export const listUsers = async () => {
  const response = await api.get("/auth/users");
  return response;
};

export const updateUserRole = async (userId, data) => {
  const response = await api.patch(`/auth/users/${userId}/role`, data);
  return response;
};

// ======================
// 📄 CLEARANCE
// ======================
export const applyClearance = async () => {
  const response = await api.post("/clearance/apply");
  return response;
};

export const getClearanceStatus = async () => {
  const response = await api.get("/clearance/status");
  return response;
};

export const getAssignedRequests = async () => {
  const response = await api.get("/clearance/assigned");
  return response;
};

export const takeAction = async (requestId, actionData) => {
  const response = await api.post(`/clearance/${requestId}/action`, actionData);
  return response;
};

// ======================
// 🎓 CERTIFICATE
// ======================
export const generateCertificate = async (requestId) => {
  const response = await api.post(`/certificate/generate/${requestId}`, {}, {
    responseType: 'blob'
  });
  return response;
};

export default api;