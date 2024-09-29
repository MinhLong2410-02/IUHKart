import React, { Suspense } from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import routes from "./pages/routes";

function App() {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    {routes.map((route, index) => (
                        <Route
                            key={index}
                            path={route.path}
                            element={React.createElement(route.element)}
                            exact={route.exact}
                        />
                    ))}
                </Routes>
            </Suspense>
        </Router>
    );
}

export default App;