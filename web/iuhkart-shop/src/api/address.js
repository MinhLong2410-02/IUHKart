import axiosClient from "./axiosClient";

export const getAllProvince = async() => {
    const data = await axiosClient.get('address/api/provinces/');
    return data
};

export const getAllDistrict = async(provinceId) => {
    const data = await axiosClient.get(`/address/api/provinces/${provinceId}/districts/`);
    return data
}

export const getAllAddress = async(districtId) => {
    const data = await axiosClient.get(`/address/api/districts/${districtId}/wards/`);
    return data
}

export const updateAddress = async(data) => {
    const res = await axiosClient.put(`/address/api/user/update_address/`, data);
    return res
}