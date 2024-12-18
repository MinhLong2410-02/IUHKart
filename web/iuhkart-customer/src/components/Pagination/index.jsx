import ReactPaginate from "react-paginate";
import { Icon } from "@iconify/react";

import "./Pagination.css";

const Pagination = (props) => {
  return (
    <ReactPaginate
      breakLabel="..."
      nextLabel={<Icon icon="ph:arrow-right-bold" />}
      previousLabel={<Icon icon="ph:arrow-left-bold" />}
      {...props}
    />
  );
};

export default Pagination;
