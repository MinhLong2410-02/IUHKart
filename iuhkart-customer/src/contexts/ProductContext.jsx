import { createContext, useState } from "react";

export const ProductContext = createContext();

export const ProductProvider = ({ children }) => {
  const [categorySelected, setCategorySelected] = useState(null);

  return (
    <ProductContext.Provider
      value={{
        categorySelected,
        setCategorySelected,
      }}
    >
      {children}
    </ProductContext.Provider>
  );
};
