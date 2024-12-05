import { createContext, useState, useEffect } from "react";

export const ProductContext = createContext();

export const ProductProvider = ({ children }) => {
  // Initialize with null instead of empty string
  const [categorySelected, setCategorySelected] = useState(null);  

  // Debug effect to track state changes
  useEffect(() => {
  }, [categorySelected]);

  const handleSetCategory = (category) => {
    setCategorySelected(String(category));
  };

  return (
    <ProductContext.Provider
      value={{
        categorySelected,
        setCategorySelected: handleSetCategory,
      }}
    >
      {children}
    </ProductContext.Provider>
  );
};
