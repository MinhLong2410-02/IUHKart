import { lazy } from "react";

export default [{
    path: "/*",
    exact: true,
    public: true,
    element: lazy(() =>
        import (".")),
}, ];