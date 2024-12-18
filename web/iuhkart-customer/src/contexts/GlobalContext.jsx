import { createContext, useState } from "react";

export const GlobalContext = createContext();

export const GlobalProvider = ({ children }) => {
  const [productID, setProductID] = useState(null);

  return (
    <GlobalContext.Provider
      value={{
        productID,
        setProductID,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};
