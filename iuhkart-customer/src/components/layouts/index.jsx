import { Outlet } from "react-router-dom";
import { Box } from "@chakra-ui/react";

import Header from "./Header";

const Layout = () => {
  return (
    <Box minHeight="100vh">
      <Header />
      <Outlet />
    </Box>
  );
};

export default Layout;
