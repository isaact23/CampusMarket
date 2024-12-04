import { createContext } from 'react';

const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
  const authApi = new AuthApi();

  return (
    <AuthContext.Provider value={{ authApi }}>
      {children}
    </AuthContext.Provider>
  );
};

export {AuthContext, AuthProvider}