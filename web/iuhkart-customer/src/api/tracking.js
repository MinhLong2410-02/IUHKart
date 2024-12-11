import { axiosClientTracking } from "./axiosClient";

const TrackingApi = {
  view: (id) => {
    const url = `track?event_type=view&product_id=${id}`;
    return axiosClientTracking.post(url);
  },
  search: (id) => {
    const url = `track?event_type=search&product_id=${id}`;
    return axiosClientTracking.post(url);
  },
  add_to_cart: (id) => {
    const url = `track?event_type=add_to_cart&product_id=${id}`;
    return axiosClientTracking.post(url);
  },
  purchase: (id) => {
    const url = `track?event_type=purchase&product_id=${id}`;
    return axiosClientTracking.post(url);
  },
};

export default TrackingApi;

