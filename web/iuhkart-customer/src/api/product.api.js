import axiosClient from "./axiosClient";

const productApi = {
  getProducts: (categoryID, page = 1, pageSize = 10) => {
    const url = `/product/api/customer?${
      categoryID ? `category_id=${categoryID}&` : ""
    }page=${page}&page_size=${pageSize}`;
    return axiosClient.get(url);
  },
  getProductByID: async (productID) => {
    const url = `/product/api/customer/view-product/${productID}`;
    
    console.log(productID);
    const dataProduct = await axiosClient.get(url);

    const trackingApi = 'https://tracking_api-iuhkart.aiclubiuh.com/api/v1/keep-track';
    console.log(dataProduct);
    const trackingData = {
      product_id: dataProduct.product_id,
      ratings: dataProduct.ratings,
      slug: dataProduct.slug,
      original_price: dataProduct.original_price,
      category_id: dataProduct.category,
      stock: dataProduct.stock,
    };
    
    await axiosClient.post(trackingApi, trackingData);

    return dataProduct;
    
  },
  getProductCategory: (categoryID) => {
    // const url = `/product/api/get-category?category_id=${categoryID}`;
    const url = `/product/api/get-category${
      categoryID ? `?category_id=${categoryID}` : ""
    }`;
    return axiosClient.get(url);
  },
};

export default productApi;
