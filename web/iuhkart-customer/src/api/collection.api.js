import axios from "axios";
import queryString from "query-string";
import Cookies from "js-cookie";

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_SEARCH_API,

  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => queryString.stringify(params),
});

axiosClient.interceptors.request.use(
  (config) => {
    const token = Cookies.get("access"); 
    if (token) {
      config.headers["access_token"] = token; // Set the 'access_token' header
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const collectionAPI = {
  search: (searchString) => {
    const url = `/collections/product/search?slug=${searchString}`;
    return axiosClient.get(url);
  },
};

export default collectionAPI;
