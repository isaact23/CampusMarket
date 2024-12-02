import { createContext, useState } from 'react';

const TokenContext = createContext(null);

const TokenProvider = ({ children }) => {
  const [token, setToken] = useState(null);

  return (
    <TokenContext.Provider value={{ token, setToken }}>
      {children}
    </TokenContext.Provider>
  );
};

export {TokenContext, TokenProvider}