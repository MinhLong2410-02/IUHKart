import { lazy } from "react";

export default [{
    path: "no",
    exact: true,
    public: true,
    element: lazy(() =>
        import (".")),
}];