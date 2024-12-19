import axiosClient, { axiosClientDashboard } from './axiosClient';

export const getDashboard = async() => {
    const url = '/metabase/api/vendor/dashboard';
    const data = await axiosClient.get(url);
    return data;
}


export const getMetaBaseDashboard = async() => {
    const url = 'dashboard';
    const data = await axiosClientDashboard.get(url);
    return data;
}