import axiosClient from './axiosClient';

const authApi = {
    login: (data) => {
        const url = '/user/api/token/vendor/';
        return axiosClient.post(url, data);
    },
};

export default authApi;


export const registerAPI = async(param) => {
    const url = 'user/api/register/vendor/';
    const data = await axiosClient.post(url, param);
    return data;
}