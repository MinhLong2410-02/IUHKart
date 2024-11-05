import { createBrowserRouter } from "react-router-dom";
import Layout from "../components/layouts";
import Home from "../pages/Home";
import ProductDetail from "../pages/ProductDetail";
import Cart from "../pages/Cart";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/products/:id",
        element: <ProductDetail />,
      },
      {
        path: "/cart",
        element: <Cart />,
      },
    ],
  },
  {
    path: "/login",
    lazy: async () => {
      const { default: Login } = await import("../pages/Login");

      return { Component: Login };
    },
  },
  {
    path: "/sign-up",
    lazy: async () => {
      const { default: SignUp } = await import("../pages/SignUp");

      return { Component: SignUp };
    },
  },
  {
    path: "*",
    lazy: async () => {
      const { default: NoMatch } = await import("../pages/404");

      return { Component: NoMatch };
    },
  },
]);

export default router;
