import axiosClient from "./axiosClient";

const authApi = {
  register: (data) => {
    const url = "/user/api/register/customer/";
    return axiosClient.post(url, data);
  },
  login: (data) => {
    const url = "/user/api/get-token/";
    return axiosClient.post(url, data);
  },
};

export default authApi;
