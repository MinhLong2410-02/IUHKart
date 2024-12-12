import axios from "axios";
import queryString from "query-string";
import Cookies from "js-cookie";

const createAxiosClient = (baseURL) => {
  const client = axios.create({
    baseURL,
    headers: {
      "Content-Type": "application/json",
    },
    paramsSerializer: (params) => queryString.stringify(params),
  });

  // Request Interceptor
  client.interceptors.request.use(
    async (config) => {
      const token = Cookies.get("access");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      console.error("Request Interceptor Error:", error);
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  client.interceptors.response.use(
    (response) => {
      // Return the full response if authorization is in headers
      if (response.headers.authorization) return response;

      // Otherwise, return the data directly
      if (response && response.data) {
        return response.data;
      }
      return response;
    },
    (error) => {
      // Handle 401 Unauthorized
      if (error?.response?.status === 401) {
        console.warn("Unauthorized - Redirecting to login");
        window.location.href = "/login";
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// Create Axios Clients
const axiosClient = createAxiosClient(process.env.DJANGO_URL);
const axiosClientTracking = createAxiosClient("https://tracking.iuhkart.systems/");

export { axiosClientTracking };
export default axiosClient;
