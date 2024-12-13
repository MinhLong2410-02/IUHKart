import { lazy } from "react";

export default [{
    path: "/sign-up-next",
    exact: true,
    public: true,
    element: lazy(() =>
        import (".")),
}];