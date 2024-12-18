import { useState, useEffect } from "react";
import { getDashboard } from "../../../api/dashboard";

export const Summary = () => {

    const [dashboard, setDashboard] = useState({});

    useEffect(() => {
        const getData = async() => {
            const dashboard = await getDashboard();
            setDashboard(dashboard)
        }
        getData();
    }, []);




    return (
        <div>
            <h2
                className="text-[30px] font-bold text-[#333] mt-[20px] mb-4 pb-[20px] border-b-2 border-black"
            >
                Summary
            </h2>
            {/* <div className="flex justify-between items-center gap-10">
                <div className="boxPrimary w-[350px] h-[280px]" dangerouslySetInnerHTML={{__html: dashboard?.iframeUrl}}>
                   
                </div>

                <div className="boxPrimary w-[350px] h-[280px]">

                </div>
                <div className="h-full flex flex-col gap-10 justify-between">
                    <div className="flex gap-10">

                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                    </div>
                    <h3>Customer Funnel - Summary based on Trace</h3>
                    <div className="flex gap-10">
                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                        <div className="boxPrimary w-[170px] h-[90px]">

                        </div>
                    </div>
                </div>

            </div>

            <div className="flex justify-between gap-10 items-center mt-10">
                <div className="boxPrimary w-[50%] h-[280px]">

                </div>

                <div className="boxPrimary w-[50%] h-[280px]">

                </div>
            </div>

            <div className="flex justify-between gap-10 items-center mt-10">
                <div className="boxPrimary w-[50%] h-[280px]">

                </div>

                <div className="w-[50%] h-[280px] flex gap-10">
                    <div className="boxPrimary w-[50%]">

                    </div>

                    <div className="boxPrimary w-[50%] ">

                    </div>
                </div>
            </div> */}
            
            

            <div className="!p-4 boxPrimary !w-full !h-[100vh]">
                <iframe 
                    src={dashboard?.iframeUrl}
                    width={"100%"}
                    height={"100%"}
                ></iframe>    
            </div>
        </div>
    );
}