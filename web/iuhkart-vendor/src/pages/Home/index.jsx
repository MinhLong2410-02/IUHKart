import { useState, useEffect } from "react";
import Cookies from 'js-cookie';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { Suspense } from 'react';
import "./main.css";
import SimpleSidebar from "./sidebar";
import { Summary } from "./components/summary";
import { Info } from "./components/info";
import { Products } from "./components/products";
import { Product } from "./components/product";


function Home() {
    useEffect(() => {
        const token = Cookies.get('authorization');
        if (!token) {
            window.location.href = '/login';
        }
    }, []);


    return (
        <div className="flex">
            <SimpleSidebar />
            <div className="home w-[100vw] min-h-[100vh] pl-[300px] pr-[50px]">
                <Routes>
                    <Route path="summary" element={<Summary />} />
                    <Route path="info" element={<Info />} />
                    <Route path="products" element={<Products />} />
                    <Route path="product/*" element={<Product />} />
                </Routes>
            </div>
        </div>
    );
}

export default Home;