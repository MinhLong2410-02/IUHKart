import { useState, useEffect } from "react";
import { getCategory, getProductDetail } from "../../../api/product";
import { useLocation } from "react-router-dom";

export const Product = () => {
    // get last part of url
    const location = useLocation();
    const id = location.pathname.split("/").pop();
    
    const [data, setData] = useState({});
    const [currentImage, setCurrentImage] = useState(0);
    const [isEdit, setIsEdit] = useState(false);
    const [category, setCategory] = useState([]);


    useEffect(() => {
        const getData = async () => {
            const data = await getProductDetail(id);
            setData(data);

            const rs = await getCategory();
            setCategory(rs);
        }

        getData();
    }, []);

    console.log(data);


    return (
        <div>
            <h2
                className="text-[30px] font-bold text-[#333] mt-[20px] mb-4 pb-[20px] border-b-2 border-black"
            >
                Product Detail
            </h2>
            <div className="!p-4 boxPrimary">
                <div className="boxPrimary flex !p-4 flex justify-center items-start gap-10">
                    <div className="flex flex-col w-[30%] gap-2">
                        <img src={data?.images?.[currentImage]?.image_url} alt="" className="w-[400px] h-[400px] mt-5" />
                        <div className="flex flex-wrap gap-2">
                            {
                                data?.images?.map((item, index) => (
                                    <img key={index} onClick={() => setCurrentImage(index)} src={item.image_url} alt="" className="w-[122px] h-[120px] cursor-pointer" />
                                ))
                            }
                        </div>
                    </div>
                    <div className="flex flex-col w-[600px] justify-start gap-3 mt-5">
                        <div className="flex justify-start items-center">
                            <span className="opacity-40 mr-2 font-bold min-w-[100px]">Tên:</span>
                            <h3 className="font-bold">{data?.product_name}</h3>
                        </div>
                        <div className="flex justify-start items-center">
                            <span className="opacity-40 mr-2 font-bold min-w-[100px]">Price:</span>
                            <h3 className="font-bold">{data?.original_price}</h3>
                        </div>
                        <div className="flex justify-start items-center">
                            <span className="opacity-40 mr-2 font-bold min-w-[100px]">Stock:</span>
                            <h3 className="font-bold">{data?.stock}</h3>
                        </div>
                        <div className="flex justify-start items-center">
                            <span className="opacity-40 mr-2 font-bold min-w-[100px]">Brand:</span>
                            <h3 className="font-bold">{data?.brand}</h3>
                        </div>
                        <div className="flex justify-start items-center">
                            <span className="opacity-40 mr-2 font-bold min-w-[100px]">Category:</span>
                            <h3 className="font-bold">{
                                category?.map((cate, index) => {
                                    if (cate?.category_id === data?.category) {
                                        return cate?.category_name;
                                    }
                                })
                            }</h3>
                        </div>
                    </div>
                    <button onClick={() => setIsEdit(true)} className="bg-[#0bc5ea] px-4 py-2 rounded mt-4 text-white font-bold">Edit</button>
                </div> 
            </div>
        </div>
    );
}