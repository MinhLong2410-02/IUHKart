import { useState } from "react";


import tempImg from "../../../assets/images/sign-ip-next-vendor.png";
import { useEffect } from "react";
import { getUserInfo, updateDOB, updateImgUser } from "../../../api/userAPI";
import { data } from "autoprefixer";
import { EditIcon } from "@chakra-ui/icons";


export const Info = () => {

    const [isEdit, setIsEdit] = useState(false);
    const [userInfo, setUserInfo] = useState({});
    const [isChange, setIsChange] = useState(false);
    const [file, setFile] = useState(null);

    useEffect(() => {
        const getData = async() => {
            const data = await getUserInfo();
            setUserInfo(data);
        }

        getData();
    }, []);

    const handleEditInfo = async () => {
        const data = {
            name: userInfo.name,
            phone: userInfo.phone,
            description: userInfo.description,
            logo_url: userInfo.logo_url,
            date_join: userInfo.date_join
        }

        console.log(file);

        try {
            if (isChange) {
                const res = await updateImgUser({
                    "logo_url": file
                });
            }
            
            // const res2 = await updateDOB({
            //     "date_of_birth": userInfo.date_join
            // });
            

            console.log(res);
            console.log(res2);
        }
        catch (err) {
            console.log(err);
        }


    }



    return (
        <div>
            <h2
                className="text-[30px] font-bold text-[#333] mt-[20px] mb-4 pb-[20px] border-b-2 border-black"
            >
                Info
            </h2>
            { !isEdit ? 
            <div className="boxPrimary !p-4 flex flex-col justify-center items-center">
                <img className="w-[250px] h-[250px] rounded-full" src={userInfo?.logo_url || tempImg} alt="img" />
                <div className="flex flex-col w-[400px] justify-start gap-3 mt-5">
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Tên:</span>
                        <h3 className="font-bold">{userInfo?.name}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Email:</span>
                        <h3 className="font-bold">{userInfo?.user?.email}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Phone:</span>
                        <h3 className="font-bold">{userInfo?.phone}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Address:</span>
                        <h3 className="font-bold">{userInfo?.user?.address}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Description:</span>
                        <h3 className="font-bold">{userInfo?.description}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Date join:</span>
                        <h3 className="font-bold">{userInfo?.date_join}</h3>
                    </div>
                </div>

                <button onClick={() => setIsEdit(true)} className="bg-[#0bc5ea] px-4 py-2 rounded mt-4 text-white font-bold">Edit</button>
            </div> 
            : 
            <div className="boxPrimary !p-4 flex flex-col justify-center items-center"> 
                    <div className="w-[250px] h-[250px] flex gap-5">
                        <input type="file" onChange={e => {
                            setFile(e.target.files[0]);
                            // console.log(e.target.files[0]);
                            setIsChange(true);
                        }} />
                        <span className="ml-2">
                            <EditIcon />
                        </span>
                    </div>
                    <div className="flex flex-col w-[400px] justify-start gap-3 mt-5">
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Tên:</span>
                        <h3 className="font-bold">{userInfo?.name}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Email:</span>
                        <h3 className="font-bold">{userInfo?.user?.email}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Phone:</span>
                        <h3 className="font-bold">{userInfo?.phone}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Address:</span>
                        <h3 className="font-bold">{userInfo?.user?.address}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Description:</span>
                        <h3 className="font-bold">{userInfo?.description}</h3>
                    </div>
                    <div className="flex justify-start items-center">
                        <span className="opacity-40 mr-2 font-bold w-[100px]">Date join:</span>
                        <input 
                            type="date"
                            className="font-bold" 
                            name="date_join"
                            defaultValue={userInfo?.date_join}
                            onChange={(e) => setUserInfo({...userInfo, date_join: e.target.value})}
                        />
                        <span className="ml-2">
                            <EditIcon />
                        </span>
                    </div>
                    </div>
                    <div className="flex gap-5">
                        <button onClick={handleEditInfo} type="submit" className="bg-[#0bc5ea] px-4 py-2 rounded mt-4 text-white font-bold">Save</button>
                        <button onClick={() => setIsEdit(false)} className="bg-[#f00] px-4 py-2 rounded mt-4 text-white font-bold ml-4">Cancel</button>
                    </div>
            </div>
            }
        </div>
    );
}