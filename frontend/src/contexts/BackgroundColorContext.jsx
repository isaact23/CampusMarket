import { createContext, useContext, useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'

const GREEN = "#569465"
const WHITE = "#FFFFFF"

const BackgroundColorContext = createContext();

const BackgroundColorProvider = ({children}) => {
    const location = useLocation()
    const [color, setColor] = useState(GREEN)

    useEffect(() => {
        if (location.pathname === '/login' || location.pathname === '/register') {
            setColor(GREEN);
        } else {
            setColor(WHITE);
        }
    }, [location]);

    return (
        <BackgroundColorContext.Provider value={color}>{children}</BackgroundColorContext.Provider>
    );
}

const useBackgroundColor = () => useContext(BackgroundColorContext)

export { BackgroundColorProvider, useBackgroundColor }