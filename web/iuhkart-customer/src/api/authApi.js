import axiosClient from "./axiosClient";

const authApi = {
  register: (data) => {
    const url = "/user/api/register/customer/";
    return axiosClient.post(url, data);
  },
  login: (data) => {
    const url = "/user/api/token/customer/";
    return axiosClient.post(url, data);
  },
  logout: (data) => {
    const url = "/user/api/token/logout/"; 
    return axiosClient.post(url, data);
  },
  getCustomerDetails: () => {
    const url = "/user/api/customer/me";
    return axiosClient.get(url); 
  },
};

export default authApi;
