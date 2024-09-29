import axiosClient from "./axiosClient";

const cartAPI = {
  addProduct: (body) => {
    const url = "/cart/api/add-product/";
    return axiosClient.post(url, body);
  },
  getCartProducts: () => {
    const url = "/cart/api/details/";
    return axiosClient.get(url);
  },
  deleteProductFromCart: (productID) => {
    const url = `/cart/api/delete-product/${productID}`;
    return axiosClient.delete(url);
  },
};

export default cartAPI;
