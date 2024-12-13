import React, { useState, useEffect } from 'react';

const Pagination = ({ total, itemsPerPage, currentPage, onPageChange }) => {
    const [pager, setPager] = useState([]);

    useEffect(() => {
        if (total > 0 && itemsPerPage > 0 && currentPage > 0) {
            let startPage, endPage;
            const totalPages = Math.ceil(total / itemsPerPage);

            if (totalPages <= 10) {
                // less than 10 total pages so show all
                startPage = 1;
                endPage = totalPages;
            } else {
                // more than 10 total pages so calculate start and end pages
                if (currentPage <= 6) {
                    startPage = 1;
                    endPage = 10;
                } else if (currentPage + 4 >= totalPages) {
                    startPage = totalPages - 9;
                    endPage = totalPages;
                } else {
                    startPage = currentPage - 5;
                    endPage = currentPage + 4;
                }
            }

            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = Math.min(startIndex + itemsPerPage - 1, total - 1);

            const pages = Array.from(Array((endPage + 1) - startPage).keys()).map(i => startPage + i);
            setPager(pages);
        }
    }, [total, itemsPerPage, currentPage]);

    return (
        <div className="flex justify-center items-center space-x-2 my-4">
            <button
                className="text-gray-800 bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded-full shadow"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}
            >
                Previous
            </button>
            {pager.map(page => (
                <button
                    key={page}
                    className={`px-3 py-1 rounded-full ${page === currentPage ? 'bg-gray-800 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300'} focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50 shadow`}
                    onClick={() => onPageChange(page)}
                >
                    {page}
                </button>
            ))}
            <button
                className="text-gray-800 bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded-full shadow"
                disabled={currentPage === pager.length}
                onClick={() => onPageChange(currentPage + 1)}
            >
                Next
            </button>
        </div>


    );
};

export default Pagination;
