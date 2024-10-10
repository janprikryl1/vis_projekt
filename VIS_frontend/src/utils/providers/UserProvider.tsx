import {createContext, useContext, useState, useEffect, ReactNode, FC} from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import {UserType} from "../types/UserType.ts";
import {saveUserDetails} from "../../api/userService.ts";

type UserContextType = {
    user: UserType | null;
    setUser: (user: UserType) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const ProviderUser: FC<{ children: ReactNode }> = ({ children }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [user, setUser] = useState<UserType | null>({
        first_name: "Jan",
        last_name: "Přikryl",
        type: "student",
        tests: []
    });
    const [loading, setLoading] = useState(!true);

    useEffect(() => {
        /*const loadIsAuthenticated = async () => {
            try {
                const result = await isAuthenticated();
                if (result) {
                    setUser(result.data.user);
                }
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
        loadIsAuthenticated();*/
    }, []);

    useEffect(() => {
        /*if (!loading) {
            const currentPath = location.pathname;
            const isProtected = PROTECTED_ROUTES.some(route => currentPath.startsWith(route.replace(':id', '')));

            if (isProtected && user === null) {
                navigate(routes.home);
            }
        }*/
    }, [loading, user, location.pathname, navigate]);


    return (
        <UserContext.Provider value={{ user, setUser }}>
            {loading ? (
                <div className="preloader">
                    <h1>Načítání...</h1>
                </div>
            ) : children}
        </UserContext.Provider>
    );
};

export const useUserContext = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a ProviderUser');
    }
    return context;
};
