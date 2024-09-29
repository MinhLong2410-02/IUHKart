import axios from "axios";
import queryString from "query-string";
import Cookies from "js-cookie";

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => queryString.stringify(params),
});

axiosClient.interceptors.request.use(async (config) => {
  const token = Cookies.get("access");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

axiosClient.interceptors.response.use(
  (res) => {
    if (res.headers.authorization) return res;
    else if (res && res.data) {
      return res.data;
    }
    return res;
  },
  (error) => {
    if (error?.response?.status === 401) {
      window.location.href = "/login";
      return;
    }

    throw error;
  }
);

export default axiosClient;
