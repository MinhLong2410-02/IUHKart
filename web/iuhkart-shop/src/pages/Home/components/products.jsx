import { useState, useEffect } from "react";
import { getCategory, getProducts } from "../../../api/product";
import { DeleteIcon, EditIcon } from "@chakra-ui/icons";
import Pagination from "./pagination";
import { Link } from "react-router-dom";





export const Products = () => {

    const [productsData, setProductsData] = useState({});
    const [pagination, setPagination] = useState({
        page: 1,
        page_size: 10
    });
    const [category, setCategory] = useState([]);

    useEffect(() => {
        const getData = async () => {
            const data = await getCategory();
            setCategory(data);
        }
        getData();
    }, []);

    useEffect(() => {
        const getData = async () => {
            const data = await getProducts({
                category_id: null,
                page: pagination.page,
                page_size: pagination.page_size
            });
            setProductsData(data);
        }
        getData();
    }, [pagination.page]);

    return (
        <div>
            <h2
                className="text-[30px] font-bold text-[#333] mt-[20px] mb-4 pb-[20px] border-b-2 border-black"
            >
                Quản lý sản phẩm
            </h2>
            <div className="!p-4 boxPrimary min-h-[80vh]">
                <div className="">
                    <div className="flex justify-between items-center">
                        <h3 className="text-[18px] font-bold text-[#333]">Tổng số lượng sản phẩm: {productsData?.count}</h3>
                    </div>
                    <div className="mt-5">
                        <table className="w-full min-w-max table-auto shadow-md bg-white">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">STT</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product name</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Brand</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {
                                    productsData?.results?.map((product, index) => (
                                        <tr key={index} className="hover:bg-gray-50">
                                            <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{index + 1}</td>
                                            <td className="px-4 py-2 whitespace-normal text-sm text-gray-500" style={{ maxWidth: "200px", lineHeight: "1.25rem" }}>
                                                {product?.product_name}
                                            </td>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{product?.original_price}</td>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{product?.stock}</td>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{product?.brand}</td>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{
                                                category?.map((cate, index) => {
                                                    if (cate?.category_id === product?.category) {
                                                        return cate?.category_name;
                                                    }
                                                })
                                            }</td>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                                <div className="flex gap-2">
                                                    <Link
                                                        to={`/product/${product?.product_id}`}
                                                        state={{ id : product?.product_id }}
                                                    >
                                                        <button className="bg-gray-200 text-gray-800 hover:bg-gray-300 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50">
                                                            <EditIcon />
                                                        </button>
                                                    </Link>
                                                    <button className="bg-red-200 text-red-800 hover:bg-red-300 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-opacity-50">
                                                        <DeleteIcon />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                }
                            </tbody>
                        </table>

                        <Pagination
                            total={productsData?.count}
                            itemsPerPage={pagination.page_size}
                            currentPage={pagination.page}
                            onPageChange={(page) => setPagination({ ...pagination, page })}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}