import axiosClient from './axiosClient';

export const getDashboard = async() => {
    const url = '/metabase/api/vendor/dashboard';
    const data = await axiosClient.get(url);
    return data;
}