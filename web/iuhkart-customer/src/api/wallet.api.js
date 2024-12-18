import axiosClient from "./axiosClient";

const walletApi = {
  addMoneyToWallet: (body) => {
    const url = "/user/api/add-money/";
    return axiosClient.put(url, body);
  },
  getWalletDetails: () => {
    const url = "/user/api/add-money";
    return axiosClient.get(url);
  },
  deleteProductFromCart: (productID) => {
    const url = `/cart/api/delete-product/${productID}`;
    return axiosClient.delete(url);
  },
};

export default walletApi;