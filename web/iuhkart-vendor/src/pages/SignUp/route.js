import {lazy} from "react";

export default [
    {
        path: "/sign-up",
        exact: true,
        public: true,
        element: lazy(() => import(".")),
    }
];
