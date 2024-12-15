import axiosClient from "./axiosClient";

const productApi = {
  getProducts: async (categoryID, page = 1, pageSize = 10) => {
    try {
      //  convert string to number
      if (categoryID == "null" || categoryID == null) {
        categoryID = "0";
        console.log("categoryID == null");
      }
      
       let url = `/product/api/customer/?page=${page}&page_size=${pageSize}`;
      if (categoryID == "0") {
      
      } else if (categoryID  ) {
        url += `&category_id=${categoryID}`;
      } else if (categoryID != null) {
        url += `&category_id=${categoryID}`;
      }


      console.log(url);
      return await axiosClient.get(url);
    } catch (error) {
      console.error(
        "Error fetching products:",
        error.response || error.message
      );
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
      console.error(
        "Error fetching product by ID:",
        error.response || error.message
      );
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
      console.error(
        "Error fetching product category:",
        error.response || error.message
      );
      throw error;
    }
  },
};

export default productApi;