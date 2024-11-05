import React, { Suspense } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import routes from "./pages/routes";
import Cookies from 'js-cookie';

function App() {
    // Replace this with your actual authentication check
    const isAuthenticated = Boolean(Cookies.get('authorization')); // Check for the 'authorization' cookie
    console.log(isAuthenticated, console.log(Cookies.get('authorization')))
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    {routes.map((route, index) => (
                        <Route
                            key={index}
                            path={route.path}
                            element={route.public || isAuthenticated ?
                                React.createElement(route.element) :
                                <Navigate to="/login" />}
                            exact={route.exact}
                        />
                    ))}
                    {/* Redirect to the home page or login based on authentication */}
                    <Route path="/" element={isAuthenticated ? <Navigate to="/home" /> : <Navigate to="/login" />} />
                    {/* Handle 404 or undefined routes */}
                    <Route path="*" element={<Navigate to={isAuthenticated ? "/home" : "/login"} />} />
                </Routes>
            </Suspense>
        </Router>
    );
}

export default App;
