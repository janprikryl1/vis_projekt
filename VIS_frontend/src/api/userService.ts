import {UserType} from "../utils/types/UserType.ts";
import axios from "axios";
import {backendURL} from "../env.ts";

export const register = async () => {

}

export const login = async () => {

}

export const isAuthenticated = async () => {

}

export const saveUserDetails = async (user: UserType) => {
    const res = axios.put(backendURL + "/user", {
        user
    });
    return await res;
}
