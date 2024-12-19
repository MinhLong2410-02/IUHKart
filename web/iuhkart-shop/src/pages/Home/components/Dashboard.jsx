import React, { useEffect, useState } from 'react';
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { use } from 'react';
import { getMetaBaseDashboard } from '../../../api/dashboard';
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);
export default function Dashboard() {
  // const dayData = {
  //   labels: ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
  //   datasets: [
  //     {
  //       label: "Doanh thu theo ngày",
  //       data: [500, 700, 400, 800, 900, 600, 1000],
  //       backgroundColor: "rgba(255, 99, 132, 0.2)",
  //       borderColor: "rgba(255, 99, 132, 1)",
  //       borderWidth: 1,
  //     },
  //   ],
  // };

  // const monthData = {
  //   labels: ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"],
  //   datasets: [
  //     {
  //       label: "Doanh thu theo tháng",
  //       data: [12000, 15000, 8000, 20000, 18000, 15000, 17000, 22000, 19000, 25000, 21000, 23000],
  //       backgroundColor: "rgba(54, 162, 235, 0.2)",
  //       borderColor: "rgba(54, 162, 235, 1)",
  //       borderWidth: 1,
  //     },
  //   ],
  // };

  // const yearData = {
  //   labels: ["2019", "2020", "2021", "2022", "2023"],
  //   datasets: [
  //     {
  //       label: "Doanh thu theo năm",
  //       data: [200000, 250000, 300000, 400000, 450000],
  //       backgroundColor: "rgba(75, 192, 192, 0.2)",
  //       borderColor: "rgba(75, 192, 192, 1)",
  //       borderWidth: 1,
  //     },
  //   ],
  // };

  // const options = {
  //   responsive: true,
  //   plugins: {
  //     legend: {
  //       position: "top",
  //     },
  //     title: {
  //       display: true,
  //     },
  //   },
  // };

  const [urlEmbed, setUrlEmbed] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const res = await getMetaBaseDashboard();
      setUrlEmbed(res?.embed_url);
      console.log(res?.embed_url);
    }

    fetchData();

  }, [])



  return (
    <div>
      <h2
        className="text-[30px] font-bold text-white mt-[20px] mb-4 pb-[20px] border-b-2 border-black"
      >
        DASHBOARD
      </h2>
      <div className="p-[20px] bg-[#2D324F] rounded-xl text-white my-10">
        <h6 className='font-bold text-[18px] mb-4'>Kết quả bán hàng</h6>
        {/* <div className="flex justify-between ">
            <div className="w-[45%] p-4 rounded-xl" style={{border:"2px solid #a7a1a1"}}>
                <p className='text-[20px] mb-2'>0 Đơn đã được bán</p>
                <h5 className='font-bold text-[22px]'>0 VND</h5>
            </div>
            <div className="w-[45%] p-4 rounded-xl" style={{border:"2px solid #a7a1a1"}}>
                <p className='text-[20px] mb-2'>0 Đơn đã huỷ</p>
                <h5 className='font-bold text-[22px]'>0 VND</h5>
            </div>
        </div> */}
        <iframe
          src={urlEmbed}
          width="100%"
          height="800"
          frameBorder="0"
          allowtransparency="true"
        ></iframe>
      </div>

      {/* <div className="p-[20px] bg-[#2D324F] rounded-xl text-white my-10">
        <h6 className='font-bold text-[18px]'>Doanh thu theo ngày</h6>
        <Bar data={dayData} options={{ ...options, plugins: { ...options.plugins, title: { text: "Doanh thu theo ngày", display: true } } }} />
      </div>

      <div className="p-[20px] bg-[#2D324F] rounded-xl text-white my-10">
        <h6 className='font-bold text-[18px]'>Doanh thu theo tháng</h6>
        <Bar data={monthData} options={{ ...options, plugins: { ...options.plugins, title: { text: "Doanh thu theo tháng", display: true } } }} />
      </div>
      <div className="p-[20px] bg-[#2D324F] rounded-xl text-white my-10">
        <h6 className='font-bold text-[18px]'>Doanh thu theo năm</h6>
        <Bar data={yearData} options={{ ...options, plugins: { ...options.plugins, title: { text: "Doanh thu theo năm", display: true } } }} />
      </div> */}
    </div>
  );
}