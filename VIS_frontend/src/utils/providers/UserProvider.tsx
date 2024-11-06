import {createContext, useContext, useState, useEffect, ReactNode, FC} from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import {isAuthenticated} from "../../api/userService.ts";
import {UserType} from "../types/UserType.ts";

type UserContextType = {
    user: UserType | undefined;
    setUser: (user: UserType) => void;
    logout: () => void;
}

const PROTECTED_ROUTES = ["/profile", "/test/:id", "/test/new_test/:id", "/question/:id", "/new_question"];

const UserContext = createContext<UserContextType | undefined>(undefined);

export const ProviderUser: FC<{ children: ReactNode }> = ({ children }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [user, setUser] = useState<UserType>();
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const loadIsAuthenticated = async () => {
            try {
                const result = await isAuthenticated();
                if (!result) return;
                setUser(result.data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
        loadIsAuthenticated();
    }, []);

    useEffect(() => {
        if (loading) {
            const currentPath = location.pathname;
            const isProtected = PROTECTED_ROUTES.some(route => currentPath.startsWith(route.replace(':id', '')));

            if (isProtected && user === undefined) {
                navigate("/");
            }
        }
    }, [loading, user, location.pathname, navigate]);

    const logout = () => {
        localStorage.removeItem("token");
        setUser(undefined);
        navigate("/");
    }

    return (
        <UserContext.Provider value={{ user, setUser, logout }}>
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
