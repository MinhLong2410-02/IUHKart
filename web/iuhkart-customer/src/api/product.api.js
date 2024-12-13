import axiosClient from "./axiosClient";

const productApi = {
  getProducts: async (categoryID, page = 1, pageSize = 10) => {
    try {
      const url = `/product/api/customer?${
        categoryID ? `category_id=${categoryID}&` : ""
      }page=${page}&page_size=${pageSize}`;
      return await axiosClient.get(url);
    } catch (error) {
      console.error("Error fetching products:", error.response || error.message);
      throw error;
    }
  },

  getProductByID: async (productID) => {
    try {
      if (!productID) {
        throw new Error("Product ID is required.");
      }

      const url = `/product/api/customer/view-product/${productID}`;
      console.log("Fetching product with ID:", productID);

      const dataProduct = await axiosClient.get(url);

      return dataProduct;
    } catch (error) {
      console.error("Error fetching product by ID:", error.response || error.message);
      throw error;
    }
  },

  getProductCategory: async (categoryID) => {
    try {
      const url = `/product/api/get-category${
        categoryID ? `?category_id=${categoryID}` : ""
      }`;
      return await axiosClient.get(url);
    } catch (error) {
      console.error("Error fetching product category:", error.response || error.message);
      throw error;
    }
  },
};

export default productApi;
