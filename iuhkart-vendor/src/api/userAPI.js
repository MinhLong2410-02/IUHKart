import axiosClient from './axiosClient';

export const getUserInfo = async() => {
    const url = 'user/api/vendor/me';
    const data = await axiosClient.get(url);
    return data;
}

export const updateImgUser = async(param) => {
    const url = 'user/api/update-image/vendor';
    const data = await axiosClient.put(url, param);
    return data;
}


export const updateDOB = async(param) => {
    const url = 'user/api/update-dob/customer';
    const data = await axiosClient.put(url, param);
    return data;
}