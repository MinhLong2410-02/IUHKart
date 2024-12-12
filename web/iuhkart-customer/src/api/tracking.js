import { axiosClientTracking } from "./axiosClient";

const TrackingApi = {
  view: (id) => {
    const url = "track";
    const body = {
      event_type: "view",
      product_ids: [id],
    };
    return axiosClientTracking.post(url, body);
  },
  search: (id) => {
    const url = "track";
    const body = {
      event_type: "search",
      product_ids: [id],
    };
    return axiosClientTracking.post(url, body);
  },
  add_to_cart: (id) => {
    const url = "track";
    const body = {
      event_type: "add_to_cart",
      product_ids: [id],
    };
    return axiosClientTracking.post(url, body);
  },
  purchase: (id) => {
    const url = "track";
    const body = {
      event_type: "purchase",
      product_ids: [id],
    };
    return axiosClientTracking.post(url, body);
  },
};

export default TrackingApi;
