import axiosClient from './axiosClient';

export const getProducts = async(param) => {
        const url = `product/api/vendor/?page=${param.page}&page_size=${param.page_size}${param.category_id ? `&category_id=${param.category_id}` : ""}`;
    const data = await axiosClient.get(url);
    return data;
}

export const getCategory = async() => {
    const url = 'product/api/get-category/';
    const data = await axiosClient.get(url);
    return data;
}

export const getProductDetail = async(id) => {
    const url = `product/api/vendor/${id}/update/`;
    const data = await axiosClient.get(url);
    return data;
}