import axios from "axios";
import queryString from "query-string";

const axiosClient = axios.create({
  baseURL: "https://qdrant-iuhkart.aiclubiuh.com/",
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => queryString.stringify(params),
});

const collectionAPI = {
  search: (searchString) => {
    const url = `/collections/product/search?slug=${searchString}`;
    return axiosClient.get(url);
  },
};

export default collectionAPI;
